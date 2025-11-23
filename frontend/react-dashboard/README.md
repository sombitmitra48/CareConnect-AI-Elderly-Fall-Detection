# CareConnect React Dashboard

## Getting Started

### Prerequisites
- Node.js 14+
- npm or yarn

### Installation

1. Navigate to the React dashboard directory:
   ```bash
   cd frontend/react-dashboard
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Application

1. Start the development server:
   ```bash
   npm start
   ```

2. Open your browser to:
   ```
   http://localhost:3000
   ```

### Building for Production

1. Create a production build:
   ```bash
   npm run build
   ```

2. The built files will be in the `build` directory.

### Project Structure

```
src/
├── components/          # React components
│   ├── Navbar.js       # Navigation bar
│   ├── Dashboard.js    # Main dashboard
│   ├── StatusCard.js   # System status component
│   ├── DetectionView.js # Live detection view
│   ├── AlertsSection.js # Alerts display
│   └── EmergencySection.js # Emergency response
├── App.js             # Main application component
├── App.css            # Main application styles
├── index.js           # Entry point
└── index.css          # Global styles
```

### Available Scripts

- `npm start`: Runs the app in development mode
- `npm test`: Launches the test runner
- `npm run build`: Builds the app for production
- `npm run eject`: Removes the single build dependency

### Learn More

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).