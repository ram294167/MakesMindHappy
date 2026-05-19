# MindPath Career Mentor — Full Stack Website

A complete, production-ready psychology-based career guidance website for students and parents.

**Tech Stack:** Next.js 16 · FastAPI · PostgreSQL · Tailwind CSS v4

---

## Project Structure

```
psychology-mentor-site/
├── frontend/          ← Next.js app (React 19, TypeScript, Tailwind v4)
├── backend/           ← FastAPI Python backend
│   ├── app/
│   │   ├── core/     ← Config / settings
│   │   ├── db/       ← Database connection
│   │   ├── models/   ← SQLAlchemy models
│   │   ├── schemas/  ← Pydantic schemas
│   │   ├── routes/   ← API endpoints
│   │   ├── services/ ← Career recommendation engine
│   │   └── main.py   ← FastAPI app entry point
│   ├── db/
│   │   ├── schema.sql ← Raw SQL schema
│   │   └── seed.py    ← Seed data script
│   └── requirements.txt
└── README.md
```

---

## Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Hero, trust, how it works, services, testimonials |
| About | `/about` | Mentor background, philosophy, credentials |
| Assessment | `/assessment` | 8-step psychometric test form |
| Results | `/results` | Sample results dashboard with charts |
| Services | `/services` | All services with detailed descriptions |
| Pricing | `/pricing` | Transparent pricing cards, WhatsApp CTA |
| FAQ | `/faq` | Accordion FAQ in categories |
| Contact | `/contact` | Contact form + details |
| Booking | `/booking` | Session booking form → WhatsApp |
| Admin | `/admin` | Dashboard: leads, assessments, bookings |

---

## Quick Start

### 1. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at **http://localhost:3000**

### 2. Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your DATABASE_URL and settings

# Start the API
uvicorn app.main:app --reload --port 8000
```

API runs at **http://localhost:8000**
API docs at **http://localhost:8000/docs**

### 3. Database

```bash
# Create the database in PostgreSQL
psql -U postgres -c "CREATE DATABASE mindpath_db;"

# Run the schema (auto-runs on startup via SQLAlchemy)
# Or manually:
psql -U postgres -d mindpath_db -f backend/db/schema.sql

# Seed initial data (testimonials, pricing, FAQs, careers)
cd backend
python -m db.seed
```

---

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/mindpath_db
ALLOWED_ORIGINS=["http://localhost:3000"]
WHATSAPP_NUMBER=919666889722
ADMIN_SECRET_KEY=your-secret-key
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WHATSAPP_NUMBER=919666889722
```

---

## API Endpoints

### Leads
- `POST /api/leads` — Capture a lead from any form
- `GET /api/leads` — List all leads (admin)
- `PATCH /api/leads/{id}/status` — Update lead status

### Assessment
- `POST /api/assessment/start` — Start + submit assessment
- `POST /api/assessment/answer` — Submit answers separately
- `GET /api/assessment/result/{id}` — Get assessment result
- `GET /api/assessment/list` — List assessments (admin)

### Bookings
- `POST /api/bookings` — Create a booking
- `GET /api/bookings` — List all bookings (admin)
- `GET /api/bookings/whatsapp-redirect` — Get WhatsApp redirect URL

### Public
- `GET /api/careers` — List career options
- `GET /api/pricing` — List pricing plans
- `GET /api/testimonials` — List testimonials
- `GET /api/faq` — List FAQs

### Admin
- `GET /api/admin/stats` — Dashboard overview stats
- `GET /api/admin/leads` — All leads
- `GET /api/admin/assessments` — All assessments
- `GET /api/admin/bookings` — All bookings

---

## WhatsApp Integration

All CTAs redirect to:
```
https://wa.me/919666889722?text=<prefilled message>
```

No payment gateway. All conversions go through WhatsApp.

---

## Deployment Notes

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (Railway / Render / DigitalOcean)
```bash
# Dockerfile or Procfile:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set `ALLOWED_ORIGINS` to your production domain.

---

## Key Features

- Mobile-first, responsive design
- Multi-step psychometric assessment (8 sections)
- Results dashboard with Recharts charts
- Lead capture on all forms
- WhatsApp CTA on every conversion point
- Admin dashboard (leads, assessments, bookings)
- Rule-based career recommendation engine (extensible to ML)
- SEO-optimised pages with metadata
- No payment gateway — all payments via WhatsApp/UPI

---

## WhatsApp Number

**+91 96668 89722** — all booking and inquiry flows lead here.
