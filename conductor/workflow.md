# Project Workflow

## Guiding Principles

1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`
2. **The Tech Stack is Deliberate:** Changes to the tech stack must be documented in `tech-stack.md` *before* implementation
3. **Test-Driven Development:** Write unit tests before implementing functionality
4. **High Code Coverage:** Aim for >80% code coverage for all modules
5. **User Experience First:** Every decision should prioritize user experience
6. **Non-Interactive & CI-Aware:** Prefer non-interactive commands. Use `CI=true` for watch-mode tools (tests, linters) to ensure single execution.

## Task Workflow

All tasks follow a strict lifecycle:

### Standard Task Workflow

1. **Select Task:** Choose the next available task from `plan.md` in sequential order

2. **Mark In Progress:** Before beginning work, edit `plan.md` and change the task from `[ ]` to `[~]`

3. **Implementation:**
   - Write the minimum amount of application code necessary to satisfy the task's requirements.
   - For TRMNL plugins, this involves editing `.liquid` and `.yml` files.

4. **Verify Locally:**
   - Run `task serve` to spin up the local TRMNL preview server.
   - Verify layout rendering by opening the browser to `http://localhost:4567/full` (or other layout paths) or curling `http://localhost:4567/render/full.html`.
   - Ensure the template parses layout classes and dynamic quote values successfully without errors.

5. **Mark Task Complete in Plan:**
   - Read `plan.md`, find the line for the completed task, and update its status from `[~]` to `[x]`.

6. **Documentation:**
   - Update `product.md` or `tech-stack.md` if any architectural or product-level decisions were made during the task.
   - Update `.trmnlp.yml.example` and `README.md` when adding or modifying plugin configuration options (custom settings) to ensure documentation matches local templates.

### Phase Completion Verification and Checkpointing Protocol

**Trigger:** This protocol is executed immediately after a task is completed that also concludes a phase in `plan.md`.

1. **Announce Protocol Start:** Inform the user that the phase is complete and the verification and checkpointing protocol has begun.

2. **List Changed Files:** Execute `git status` to see all files modified during this phase.

3. **Verify and Create Tests:**
   - TRMNL plugins typically use Liquid. If a testing framework is introduced (e.g., for liquid rendering), ensure tests are updated.
   - Target: >80% coverage if applicable.

4. **Execute Automated Tests (if any):**
   - Run `npm test` or the identified test command.
   - If tests fail, inform the user and begin debugging.

5. **Propose a Detailed, Actionable Manual Verification Plan:**
   - Generate a step-by-step plan for the user to verify the phase's goals within the TRMNL environment.

6. **Await Explicit User Feedback:**
   - **PAUSE** and await the user's response. Do not proceed without an explicit yes or confirmation.

7. **Create Checkpoint Commit:**
   - Stage all changes for the entire phase, including code and `plan.md`.
   - Perform a single commit for the phase (e.g., `feat: Complete Phase 1 - Core Layouts`).

8. **Attach Phase Summary with Git Notes:**
   - **Step 8.1: Get Commit Hash:** Obtain the hash of the checkpoint commit.
   - **Step 8.2: Draft Note Content:** Create a detailed summary for the completed phase, listing all tasks finished and the overall impact.
   - **Step 8.3: Attach Note:** Use `git notes add -m "<note content>" <commit_hash>`.

9. **Record Phase Checkpoint SHA in Plan:**
   - Update `plan.md` to record the SHA next to the phase heading.

10. **Announce Completion:** Inform the user that the phase is complete and the checkpoint has been created.

### Quality Gates

Before marking any task complete, verify:

- [ ] All tests pass
- [ ] Code coverage meets requirements (>80%)
- [ ] Code follows project's code style guidelines (as defined in `code_styleguides/`)
- [ ] All public functions/methods are documented (e.g., docstrings, JSDoc, GoDoc)
- [ ] Type safety is enforced (e.g., type hints, TypeScript types, Go types)
- [ ] No linting or static analysis errors (using the project's configured tools)
- [ ] Works correctly on mobile (if applicable)
- [ ] Documentation updated if needed (including `README.md` and `.trmnlp.yml.example` when configuration settings change)
- [ ] No security vulnerabilities introduced

## Development & Usage

### "Building"
There is no compilation step. The source code *is* the distribution.
To "deploy" or "install":
1.  The `src/` directory is the plugin bundle.
2.  In a standard TRMNL development setup, this folder would be copied to the user's plugins directory.

### Running/Testing
*   **Local Testing:** Since this relies on the TRMNL environment to parse `settings.yml` and render `.liquid` with the fetched data, local testing typically requires a TRMNL simulator or uploading the plugin to a private TRMNL account.
*   **Data Flow:**
    1.  TRMNL reads `settings.yml`.
    2.  It constructs the polling URL using the user-provided `spreadsheet_id`.
    3.  It fetches the CSV data.
    4.  It passes the data to the `.liquid` templates to render the image.

## Testing Requirements

### Unit Testing
- Every module must have corresponding tests.
- Use appropriate test setup/teardown mechanisms (e.g., fixtures, beforeEach/afterEach).
- Mock external dependencies.
- Test both success and failure cases.

### Integration Testing
- Test complete user flows
- Verify database transactions
- Test authentication and authorization
- Check form submissions

### Mobile Testing
- Test on actual iPhone when possible
- Use Safari developer tools
- Test touch interactions
- Verify responsive layouts
- Check performance on 3G/4G

## Code Review Process

### Self-Review Checklist
Before requesting review:

1. **Functionality**
   - Feature works as specified
   - Edge cases handled
   - Error messages are user-friendly

2. **Code Quality**
   - Follows style guide
   - DRY principle applied
   - Clear variable/function names
   - Appropriate comments

3. **Testing**
   - Unit tests comprehensive
   - Integration tests pass
   - Coverage adequate (>80%)

4. **Security**
   - No hardcoded secrets
   - Input validation present
   - SQL injection prevented
   - XSS protection in place

5. **Performance**
   - Database queries optimized
   - Images optimized
   - Caching implemented where needed

6. **Mobile Experience**
   - Touch targets adequate (44x44px)
   - Text readable without zooming
   - Performance acceptable on mobile
   - Interactions feel native

## Commit Guidelines

### Message Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Maintenance tasks

### Examples
```bash
git commit -m "feat(auth): Add remember me functionality"
git commit -m "fix(posts): Correct excerpt generation for short posts"
git commit -m "test(comments): Add tests for emoji reaction limits"
git commit -m "style(mobile): Improve button touch targets"
```

## Definition of Done

A task is complete when:

1. All code implemented to specification
2. Unit tests written and passing
3. Code coverage meets project requirements
4. Documentation complete (if applicable)
5. Code passes all configured linting and static analysis checks
6. Works beautifully on mobile (if applicable)
7. Implementation notes added to `plan.md`
8. Changes committed with proper message
9. Git note with task summary attached to the commit

## Emergency Procedures

### Critical Bug in Production
1. Create hotfix branch from main
2. Write failing test for bug
3. Implement minimal fix
4. Test thoroughly including mobile
5. Deploy immediately
6. Document in plan.md

### Data Loss
1. Stop all write operations
2. Restore from latest backup
3. Verify data integrity
4. Document incident
5. Update backup procedures

### Security Breach
1. Rotate all secrets immediately
2. Review access logs
3. Patch vulnerability
4. Notify affected users (if any)
5. Document and update security procedures

## Deployment Workflow

### Pre-Deployment Checklist
- [ ] All tests passing
- [ ] Coverage >80%
- [ ] No linting errors
- [ ] Mobile testing complete
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Backup created

### Deployment Steps
1. Merge feature branch to main
2. Tag release with semantic versioning prefixed by a `v` (e.g., `v1.0.0`)
3. Push to deployment service
4. Run database migrations
5. Verify deployment
6. Test critical paths
7. Monitor for errors

### Post-Deployment
1. Monitor analytics
2. Check error logs
3. Gather user feedback
4. Plan next iteration

## Continuous Improvement

- Review workflow weekly
- Update based on pain points
- Document lessons learned
- Optimize for user happiness
- Keep things simple and maintainable

## Common Tasks
*   **Update Layout:** Modify `src/*.liquid` files.
*   **Change Data Source Logic:** Edit the `polling_url` or `custom_fields` in `src/settings.yml`.
*   **Update Metadata:** Update `src/settings.yml` (description, author) and `package.json`.
