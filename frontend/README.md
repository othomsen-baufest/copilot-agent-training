# Frontend — Angular Application

A Stripe-inspired Angular application that provides authentication and a protected welcome dashboard.

## Tech Stack

- **Angular 19** (module-based, no standalone components)
- **ReactiveFormsModule** for form handling
- **HttpClientModule** for API calls
- **SessionStorage** for token persistence

## Design System

Follows the Stripe-inspired design language defined in `DESIGN.md`:
- Font: Inter (Google Fonts) at weight 300/400 with `font-feature-settings: "ss01"`
- Primary color: `#533afd` (indigo)
- Gradient-mesh backdrop on auth surfaces
- Pill-shaped buttons (`border-radius: 9999px`)
- Form inputs with `border-radius: 6px`

## Getting Started

### Prerequisites
- Node.js ≥ 18
- Angular CLI 19 (`npm install -g @angular/cli@19`)
- Backend running at `http://localhost:8000`

### Install dependencies

```bash
npm install
```

### Development server

```bash
npm start
# or (proxy is already configured in angular.json)
ng serve
```

Navigate to `http://localhost:4200`.

### Production build

```bash
npm run build
```

## Project Structure

```
src/
├── app/
│   ├── guards/
│   │   └── auth.guard.ts          # CanActivate — redirects to /login if not authenticated
│   ├── pages/
│   │   ├── login/                 # /login route
│   │   └── welcome/               # /welcome route (protected)
│   ├── services/
│   │   └── auth.service.ts        # Login / logout / token management
│   ├── app-routing.module.ts
│   ├── app.component.*
│   └── app.module.ts
├── environments/
│   └── environment.ts
└── styles.css
```

## Routes

| Path | Component | Guard |
|------|-----------|-------|
| `/` | → redirect to `/welcome` | — |
| `/login` | `LoginComponent` | Redirects to `/welcome` if logged in |
| `/welcome` | `WelcomeComponent` | `AuthGuard` — requires token |
| `/**` | → redirect to `/welcome` | — |

## API Integration

The proxy configuration in `proxy.conf.json` forwards `/api/*` requests to `http://localhost:8000/*`.

### Login
- **Endpoint**: `POST /api/auth/token`
- **Body**: `{ "username": "string", "password": "string" }`
- **Response**: `{ "access_token": "...", "token_type": "bearer", "expires_in": 300 }`
- Token is stored in `sessionStorage` under key `auth_token`.

### Test credentials
- Username: `admin`
- Password: `admin123`

## Auth Service API

| Method | Description |
|--------|-------------|
| `login(username, password)` | POST to `/api/auth/token`, stores token in sessionStorage |
| `logout()` | Removes token from sessionStorage |
| `isLoggedIn()` | Returns `true` if token present in sessionStorage |
| `getToken()` | Returns token string or null |
