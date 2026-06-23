#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'

SETTINGS_FILE = File.expand_path('../../../../src/settings.yml', __dir__)

def load_settings
  unless File.exist?(SETTINGS_FILE)
    puts "Error: settings.yml not found at #{SETTINGS_FILE}"
    exit 1
  end
  begin
    YAML.load_file(SETTINGS_FILE)
  rescue => e
    puts "Error parsing YAML: #{e.message}"
    exit 1
  end
end

def verify(target_version = nil)
  settings = load_settings
  current_version = settings['framework_version']
  
  if current_version.nil?
    puts "Verification Failed: 'framework_version' is not set in settings.yml."
    return false
  end

  puts "Current framework version: #{current_version}"
  
  if target_version && current_version.to_s != target_version.to_s
    puts "Verification Failed: version is #{current_version}, expected #{target_version}."
    return false
  end

  puts "Verification Successful!"
  true
end

def update(new_version)
  unless File.exist?(SETTINGS_FILE)
    puts "Error: settings.yml not found at #{SETTINGS_FILE}"
    exit 1
  end

  content = File.read(SETTINGS_FILE)
  
  if content =~ /^framework_version:/
    content.sub!(/^framework_version:.*$/, "framework_version: #{new_version}")
  else
    if content =~ /^strategy:.*$/
      content.sub!(/^(strategy:.*)$/, "\\1\nframework_version: #{new_version}")
    else
      content = "framework_version: #{new_version}\n" + content
    end
  end

  File.write(SETTINGS_FILE, content)
  puts "Successfully updated framework_version to #{new_version} in settings.yml."
end

command = ARGV[0]
arg = ARGV[1]

case command
when 'verify'
  success = verify(arg)
  exit(success ? 0 : 1)
when 'update'
  if arg.nil?
    puts "Usage: ruby manage_framework.rb update <version>"
    exit 1
  end
  update(arg)
else
  puts "Usage: ruby manage_framework.rb [verify|update] <version>"
  exit 1
end
