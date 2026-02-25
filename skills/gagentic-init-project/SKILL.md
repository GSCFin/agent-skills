---
name: gagentic-init-project
description: Interactive skill to initialize a new project workspace by selecting a tech stack and automatically symlinking the appropriate agent skills into the `.agent/skills/` directory.
---

# gagentic-init-project

This skill helps users bootstrap a new project workspace by setting up the necessary agent skills as symlinks in the `.agent/skills/` directory based on the chosen technology stack.

## Usage Instructions

When the user invokes this skill, follow these steps:

1. **Ask for the Tech Stack:** If the user hasn't provided a specific tech stack, ask them to choose from the following supported stacks:
   - `modern-web` (React, Next.js, Tailwind, Web Design)
   - `react-native` (React Native, Mobile App Development)
   - `backend-node` (Node.js, Express/Nest, API Design)
   - `backend-go` (Golang, API Design, Architecture)
   - `backend-rust` (Rust, Systems, API Design)
   - `backend-python` (Python, FastAPI, API Design)
   - `3d-gamedev` (Three.js, WebGL, Game Architecture, Unity)
   - `fullstack-nextjs` (Next.js, Node.js, Database, Architecture, Tailwind)

2. **Map the Stack to Skills:** Use the following mapping to determine which skills to symlink from the central repository (`~/INFCAP/agenticse/agenticse-agent-skills/skills/`):
   - **`modern-web`**:
     - `react-best-practices`
     - `nextjs-best-practices`
     - `nextjs-app-router-patterns`
     - `tailwind-design-system`
     - `ui-ux-pro-max`
     - `agenticse-design-system`
     - `clean-code`

   - **`react-native`**:
     - `react-native-architecture`
     - `mobile-developer`
     - `mobile-design`
     - `react-best-practices`
     - `clean-code`

   - **`backend-node`**:
     - `nodejs-backend-patterns`
     - `nodejs-best-practices`
     - `backend-architect`
     - `api-design-principles`
     - `clean-code`
     - `architecture`

   - **`backend-go`**:
     - `golang-pro`
     - `go-concurrency-patterns`
     - `backend-architect`
     - `api-design-principles`
     - `clean-code`
     - `architecture`

   - **`backend-rust`**:
     - `rust-pro`
     - `rust-system-architecture-design`
     - `rust-async-patterns`
     - `backend-architect`
     - `api-design-principles`
     - `clean-code`
     - `architecture`

   - **`backend-python`**:
     - `python-pro`
     - `fastapi-pro`
     - `python-patterns`
     - `backend-architect`
     - `api-design-principles`
     - `clean-code`
     - `architecture`

   - **`3d-gamedev`**:
     - `game-development`
     - `threejs-skills`
     - `3d-web-experience`
     - `react-best-practices`
     - `c4-architecture-c4-architecture`
     - `clean-code`

   - **`fullstack-nextjs`**:
     - `react-best-practices`
     - `nextjs-best-practices`
     - `nodejs-backend-patterns`
     - `database-design`
     - `backend-architect`
     - `architecture`
     - `clean-code`
     - `tailwind-design-system`
     - `ui-ux-pro-max`

3. **Execute Symlink Commands:** Once the stack is identified, generate and run the necessary `ln -s` commands to link these skills into the user's current project under `.agent/skills/`.

   _Example Command Structure:_

   ```bash
   mkdir -p .agent/skills
   cd .agent/skills
   ln -s ~/INFCAP/agenticse/agenticse-agent-skills/skills/<skill-name> .
   # Repeat for each required skill...
   ```

4. **Confirm Success:** Verify the symlinks using `ls -la .agent/skills` and present a summarizing message to the user confirming the initialized skills.

## Guidelines

- Always ensure the `.agent/skills` directory exists before creating symlinks.
- Always use the absolute path `~/INFCAP/agenticse/agenticse-agent-skills/skills/<skill-name>` as the target.
- If the user requests a custom stack or additional skills, accommodate them by looking up relevant skills from the central repository before executing.
