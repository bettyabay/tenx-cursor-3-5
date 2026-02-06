# Project Chimera Frontend

Next.js frontend application for Project Chimera - Autonomous AI Influencer Factory.

## Features

- 📊 **Dashboard** - Overview of system status, trends, and agents
- 📈 **Trends Page** - View trending topics from social media platforms
- 🤖 **Agents Page** - Monitor and manage autonomous AI agents
- 🔗 **API Integration** - Connects to FastAPI backend
- 🎨 **Modern UI** - Built with Next.js, TypeScript, and Tailwind CSS

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install
# or
yarn install
```

### Development

```bash
# Start development server
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
# Build for production
npm run build
# or
yarn build

# Start production server
npm start
# or
yarn start
```

## Project Structure

```
frontend/
├── app/              # Next.js app directory
│   ├── page.tsx     # Dashboard (home page)
│   ├── trends/      # Trends page
│   ├── agents/      # Agents page
│   └── layout.tsx   # Root layout
├── components/       # React components
│   ├── TrendCard.tsx
│   ├── AgentCard.tsx
│   └── StatusBadge.tsx
├── lib/              # Utilities
│   └── api.ts       # API client
└── public/           # Static assets
```

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000` by default.

To change the API URL, set the environment variable:

```bash
NEXT_PUBLIC_API_URL=http://your-api-url:8000
```

## Features

### Dashboard
- System health status
- Quick stats (trends count, agents count)
- Recent trends preview
- Active agents preview

### Trends Page
- List all trending topics
- Filter by platform
- View engagement metrics
- Relevance scores

### Agents Page
- List all registered agents
- View agent status
- See agent capabilities
- Check OpenClaw registration status

## Development Notes

- Uses React Query for data fetching
- TypeScript for type safety
- Tailwind CSS for styling
- Responsive design (mobile-friendly)

## Troubleshooting

### API Connection Issues

If you see "Unable to connect to API":
1. Make sure the backend is running: `python scripts/run_api.py`
2. Check that the API is accessible at http://localhost:8000
3. Verify CORS settings in the backend allow requests from http://localhost:3000

### Empty Data

The API endpoints return empty data until implementations are complete. This is expected behavior - the frontend is ready and will display data once the backend is fully implemented.
