# Agent Orchestration Landing Page

This package contains a Next.js App Router project that renders a security-focused landing page using [Saas UI](https://saas-ui.dev) and Chakra UI. It is designed to complement the existing agent orchestration service by providing a polished marketing surface with feature highlights, testimonials, and pricing tiers.

## Getting started

1. Install dependencies:

   ```bash
   pnpm install
   # or
   npm install
   # or
   yarn install
   ```

2. Run the development server:

   ```bash
   pnpm dev
   # or
   npm run dev
   # or
   yarn dev
   ```

   Then open [http://localhost:3000](http://localhost:3000) in your browser.

3. Build for production:

   ```bash
   pnpm build
   pnpm start
   ```

## Security defaults

- React Strict Mode is enabled to surface side effects early.
- Chakra UI and Saas UI providers are configured to avoid hydration mismatches and respect the declared color mode.
- Dependencies are pinned to modern, actively maintained versions compatible with Next.js 14.

Please audit and update environment-specific configuration (analytics, auth, etc.) before deploying to production.
