# Employee Database - React Frontend

This is a React frontend for the Employee Database application.

## Setup Instructions

### Prerequisites
- Node.js and npm installed

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

### Running the Application

1. Make sure your Flask backend is running on `http://localhost:80`

2. Start the React development server:
```bash
npm start
```

The application will open in your browser at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## Features

- **Add Employee**: Add new employees with their information and image
- **Get Employee**: Retrieve employee information by ID
- **Image Upload**: Upload employee images to S3
- **Database Integration**: Connected to MySQL RDS and DynamoDB

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── index.css
├── src/
│   ├── components/
│   │   ├── AddEmp.js
│   │   ├── GetEmp.js
│   │   ├── AddEmpOutput.js
│   │   └── GetEmpOutput.js
│   ├── App.js
│   └── index.js
├── package.json
└── README.md
```

## API Endpoints

- `POST /addemp` - Add new employee
- `POST /fetchdata` - Fetch employee data by ID
- `GET /getemp` - Get the form to fetch employee
