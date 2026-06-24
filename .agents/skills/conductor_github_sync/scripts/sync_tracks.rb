#!/usr/bin/env ruby
# frozen_string_literal: true

require 'json'
require 'fileutils'
require 'open3'
require 'date'
require 'shellwords'

REPO_ROOT = File.expand_path('../../../../', __dir__)
TRACKS_DIR = File.join(REPO_ROOT, 'conductor/tracks')
ARCHIVE_DIR = File.join(REPO_ROOT, 'conductor/archive')
TRACKS_FILE = File.join(REPO_ROOT, 'conductor/tracks.md')

# Helper to run system commands safely
def run_cmd(cmd, env = {})
  stdout, stderr, status = Open3.capture3(env, cmd, chdir: REPO_ROOT)
  unless status.success?
    puts "Error running command: #{cmd}\nStderr: #{stderr}"
  end
  [stdout, status.success?]
end

# Check if GH CLI is installed and authenticated
def check_gh
  stdout, success = run_cmd("gh auth status")
  unless success
    puts "Error: GitHub CLI (gh) is not authenticated. Please run 'gh auth login' or set GH_TOKEN."
    exit 1
  end
end

# Load all tracks from both active tracks and archive
def load_all_tracks
  tracks = []
  [TRACKS_DIR, ARCHIVE_DIR].each do |dir|
    next unless Dir.exist?(dir)
    Dir.glob(File.join(dir, '*/metadata.json')).each do |meta_path|
      begin
        meta = JSON.parse(File.read(meta_path))
        meta['file_path'] = meta_path
        meta['dir_path'] = File.dirname(meta_path)
        tracks << meta
      rescue => e
        puts "Warning: Failed to parse metadata at #{meta_path}: #{e.message}"
      end
    end
  end
  tracks
end

# Get all open/closed GitHub issues
def fetch_gh_issues
  stdout, success = run_cmd("gh issue list --state all --json number,title,body --limit 100")
  return [] unless success
  JSON.parse(stdout)
end

# Create a new GitHub issue from a track
def create_issue_from_track(track)
  spec_path = File.join(track['dir_path'], 'spec.md')
  unless File.exist?(spec_path)
    puts "Warning: spec.md not found for track #{track['track_id']}"
    return nil
  end

  spec_content = File.read(spec_path)
  
  # Parse title and body from spec.md
  title = track['description']
  if spec_content =~ /^#\s+Specification\s+-\s+(.+)$/
    title = $1.strip
  end

  # The body is everything starting from ## Overview to end
  body = spec_content
  if spec_content =~ /(##\s+Overview.*)$/m
    body = $1.strip
  end

  # Title prefix to match Conductor tracks pattern
  issue_title = "Track: #{title}"
  
  puts "Creating GitHub issue for track '#{title}'..."
  cmd = "gh issue create --title #{Shellwords.escape(issue_title)} --body #{Shellwords.escape(body)}"
  stdout, success = run_cmd(cmd)
  if success && stdout =~ %r{/issues/(\d+)}
    issue_num = $1.to_i
    puts "Successfully created issue ##{issue_num} for track #{track['track_id']}."
    issue_num
  else
    puts "Error: Failed to create issue for #{track['track_id']}."
    nil
  end
end

# Update track's metadata.json with the GitHub issue number
def update_track_metadata(track, issue_num)
  meta_path = track['file_path']
  meta = JSON.parse(File.read(meta_path))
  meta['github_issue_number'] = issue_num
  meta['updated_at'] = Time.now.utc.strftime("%Y-%m-%dT%H:%M:%SZ")
  
  # Save back with pretty formatting
  File.write(meta_path, JSON.pretty_generate(meta) + "\n")
  puts "Updated metadata for #{track['track_id']} with GitHub Issue ##{issue_num}."
end

# Sync Tracks to Issues
def sync_tracks_to_issues
  tracks = load_all_tracks
  gh_issues = fetch_gh_issues

  tracks.each do |track|
    # Skip if already has issue number
    next if track['github_issue_number']

    # Search for existing issues by title
    track_title = track['description']
    spec_path = File.join(track['dir_path'], 'spec.md')
    if File.exist?(spec_path) && File.read(spec_path) =~ /^#\s+Specification\s+-\s+(.+)$/
      track_title = $1.strip
    end

    matched_issue = gh_issues.find do |issue|
      issue['title'].casecmp("Track: #{track_title}") == 0 ||
        issue['title'].casecmp(track_title) == 0
    end

    if matched_issue
      update_track_metadata(track, matched_issue['number'].to_i)
    else
      issue_num = create_issue_from_track(track)
      if issue_num
        update_track_metadata(track, issue_num)
      end
    end
  end
end

# Sync Issues to Tracks
def sync_issues_to_tracks(auto_confirm = false)
  tracks = load_all_tracks
  gh_issues = fetch_gh_issues

  # Filter issues that are NOT mapped to any track
  unmapped_issues = gh_issues.select do |issue|
    tracks.none? { |t| t['github_issue_number'] == issue['number'].to_i }
  end

  if unmapped_issues.empty?
    puts "No unmapped issues to import."
    return
  end

  unmapped_issues.each do |issue|
    title = issue['title']
    number = issue['number']
    
    # We want issues that represent features, bug fixes, or tracks.
    # If the title starts with "Track: ", we definitely import it.
    # Otherwise, ask/verify if user wants to import.
    clean_title = title.sub(/^Track:\s+/i, '')
    
    puts "Found unmapped issue ##{number}: '#{title}'"
    unless auto_confirm
      print "Do you want to import this issue as a Conductor track? (y/n): "
      ans = gets.strip.downcase
      next unless ans == 'y' || ans == 'yes'
    end

    import_issue_as_track(issue, clean_title)
  end
end

# Import a single issue as a track
def import_issue_as_track(issue, clean_title)
  number = issue['number']
  body = issue['body'] || "No description provided."

  # Generate unique track ID from clean title
  # Replace non-alphanumeric with underscores and append current date
  slug = clean_title.downcase.gsub(/[^a-z0-9]+/, '_').gsub(/^_+|_+$/, '')
  date_str = Time.now.strftime("%Y%m%d")
  track_id = "#{slug}_#{date_str}"
  
  track_dir = File.join(TRACKS_DIR, track_id)
  
  if Dir.exist?(track_dir)
    puts "Track directory #{track_id} already exists. Skipping."
    return
  end

  FileUtils.mkdir_p(track_dir)
  puts "Created track directory: #{track_dir}"

  # Create metadata.json
  meta = {
    "track_id" => track_id,
    "type" => "feature",
    "status" => "new",
    "created_at" => Time.now.utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "updated_at" => Time.now.utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "description" => clean_title,
    "github_issue_number" => number.to_i
  }
  File.write(File.join(track_dir, 'metadata.json'), JSON.pretty_generate(meta) + "\n")

  # Create spec.md
  spec_content = <<~SPEC
    # Specification - #{clean_title}

    ## Overview
    #{body}

    ## Acceptance Criteria
    - [ ] Verify imported issue requirements.
  SPEC
  File.write(File.join(track_dir, 'spec.md'), spec_content)

  # Create plan.md
  plan_content = <<~PLAN
    # Implementation Plan - #{clean_title}

    This plan outlines the steps to implement the track imported from GitHub Issue ##{number}.

    ## Phase 1: Core Implementation
    - [ ] Task: Implement requirements from Issue ##{number}
    - [ ] Task: Conductor - User Manual Verification 'Phase 1'
  PLAN
  File.write(File.join(track_dir, 'plan.md'), plan_content)

  # Create index.md
  index_content = <<~INDEX
    # Track Index - #{clean_title}

    - [Specification](./spec.md)
    - [Implementation Plan](./plan.md)
  INDEX
  File.write(File.join(track_dir, 'index.md'), index_content)

  # Register in tracks.md
  if File.exist?(TRACKS_FILE)
    tracks_content = File.read(TRACKS_FILE)
    
    # We construct the track markdown block
    track_block = <<~BLOCK

      ---

      - [ ] **Track: #{clean_title}**
      *Link: [./tracks/#{track_id}/](./tracks/#{track_id}/)*
    BLOCK

    # Append before the last text or just append at the end
    File.write(TRACKS_FILE, tracks_content.strip + "\n" + track_block)
    puts "Registered track '#{clean_title}' in tracks.md."
  else
    puts "Warning: tracks.md not found at #{TRACKS_FILE}. Cannot register track."
  end
end

# Close issues of completed/archived tracks
def close_completed_track_issues
  tracks = load_all_tracks
  
  # Completed/archived tracks are those located in ARCHIVE_DIR
  archived_tracks = tracks.select { |t| t['dir_path'].start_with?(ARCHIVE_DIR) }
  
  if archived_tracks.empty?
    puts "No archived tracks found to check for issue closing."
    return
  end

  archived_tracks.each do |track|
    issue_num = track['github_issue_number']
    next unless issue_num

    # Get issue state
    stdout, success = run_cmd("gh issue view #{issue_num} --json state")
    next unless success

    begin
      data = JSON.parse(stdout)
      if data['state'] == 'OPEN'
        puts "Found open issue ##{issue_num} for archived/completed track '#{track['description']}'."
        close_cmd = "gh issue close #{issue_num} --reason completed --comment \"Closed automatically via Conductor sync task (track completed & archived).\""
        _, close_success = run_cmd(close_cmd)
        if close_success
          puts "Successfully closed GitHub Issue ##{issue_num}."
        else
          puts "Failed to close GitHub Issue ##{issue_num}."
        end
      end
    rescue => e
      puts "Error checking/closing issue ##{issue_num}: #{e.message}"
    end
  end
end

# Main routing logic
check_gh

command = ARGV[0] || 'sync'
case command
when 'sync'
  puts "Syncing tracks to GitHub issues..."
  sync_tracks_to_issues
  puts "\nSyncing GitHub issues to tracks..."
  sync_issues_to_tracks
  puts "\nChecking for completed/archived tracks to close issues..."
  close_completed_track_issues
when 'tracks-to-issues'
  sync_tracks_to_issues
when 'issues-to-tracks'
  sync_issues_to_tracks
when 'issues-to-tracks-auto'
  sync_issues_to_tracks(true)
when 'close-completed'
  close_completed_track_issues
else
  puts "Usage: ruby sync_tracks.rb [sync|tracks-to-issues|issues-to-tracks|issues-to-tracks-auto|close-completed]"
  exit 1
end
