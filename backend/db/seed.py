"""
Seed script — populates the database with initial data.
Run: python -m db.seed
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal, engine
from app.models.models import Base, Testimonial, FAQ, CareerOption, PricingPlan


def seed_testimonials(db):
    testimonials = [
        {
            "name": "Priya S.",
            "role": "Class 12 Student, Hyderabad",
            "text": "I was completely confused between Science and Commerce. After the assessment and the session with the mentor, I felt like someone finally understood what I was going through. I chose Commerce and I love it now.",
            "stars": 5,
            "emoji": "🎓",
        },
        {
            "name": "Ravi Kumar",
            "role": "Parent of a Class 11 Student",
            "text": "My son wasn't sure what he wanted. We tried talking to school teachers but got generic answers. The psychometric test was eye-opening. The mentor explained everything clearly and gave us a real plan.",
            "stars": 5,
            "emoji": "👨‍👩‍👦",
        },
        {
            "name": "Ananya M.",
            "role": "First-year Engineering Student",
            "text": "I was already in Engineering but felt miserable. The session helped me understand my actual strengths. I am now planning a switch to design and I feel so much better.",
            "stars": 5,
            "emoji": "💡",
        },
        {
            "name": "Karthik R.",
            "role": "Class 10 Student, Chennai",
            "text": "Didn't know if I should pick PCM or PCB. The aptitude test showed exactly where my strengths are. Now I have chosen PCB and I am confident about it.",
            "stars": 5,
            "emoji": "📚",
        },
        {
            "name": "Sneha P.",
            "role": "Parent, Bangalore",
            "text": "The mentor was patient, honest, and practical. No empty promises. Just clear guidance. My daughter now knows her career direction and is motivated.",
            "stars": 5,
            "emoji": "🌟",
        },
    ]
    for t in testimonials:
        db.add(Testimonial(**t))
    print("✓ Testimonials seeded")


def seed_faqs(db):
    faqs = [
        {
            "category": "About the Assessment",
            "question": "Who should take this test?",
            "answer": "Any student who is unsure about their career path, stream selection, or college choice. Works best for students in Class 9–12, college students, and gap year students.",
            "order_index": 1,
        },
        {
            "category": "About the Assessment",
            "question": "How long does the assessment take?",
            "answer": "Approximately 25–35 minutes. No time pressure — you go at your own pace.",
            "order_index": 2,
        },
        {
            "category": "Payments & Booking",
            "question": "Do I need to pay online?",
            "answer": "No. There is no online payment gateway. Payment is made via UPI/bank transfer after connecting on WhatsApp.",
            "order_index": 3,
        },
        {
            "category": "Payments & Booking",
            "question": "How do I connect with the mentor?",
            "answer": "Click any WhatsApp button on the website. You will be connected directly to the mentor.",
            "order_index": 4,
        },
        {
            "category": "The Process",
            "question": "Can parents also join the session?",
            "answer": "Yes, and it is encouraged. Parents can join the mentoring session. There is also a separate Parent Counselling Session available.",
            "order_index": 5,
        },
    ]
    for f in faqs:
        db.add(FAQ(**f))
    print("✓ FAQs seeded")


def seed_careers(db):
    careers = [
        {
            "title": "Psychologist / Counsellor",
            "emoji": "🧠",
            "description": "Help people understand themselves and navigate life challenges.",
            "suitable_streams": ["Arts", "Science (Psychology)"],
            "required_strengths": ["Empathy", "Listening", "Analytical thinking"],
            "interest_areas": ["helping", "social", "humanities"],
        },
        {
            "title": "Software Engineer",
            "emoji": "💻",
            "description": "Build software, apps, and systems that solve real problems.",
            "suitable_streams": ["Science (PCM)"],
            "required_strengths": ["Logical thinking", "Problem solving"],
            "interest_areas": ["technology", "logic", "building"],
        },
        {
            "title": "Business / Entrepreneur",
            "emoji": "🚀",
            "description": "Start or run organisations, lead teams, and create value.",
            "suitable_streams": ["Commerce", "Any stream"],
            "required_strengths": ["Leadership", "Communication"],
            "interest_areas": ["business", "leadership", "finance"],
        },
        {
            "title": "Doctor / Medical Professional",
            "emoji": "⚕️",
            "description": "Diagnose and treat illness. Help people heal.",
            "suitable_streams": ["Science (PCB)"],
            "required_strengths": ["Attention to detail", "Empathy"],
            "interest_areas": ["science", "helping"],
        },
        {
            "title": "UX / Product Designer",
            "emoji": "🎨",
            "description": "Design intuitive, beautiful digital experiences.",
            "suitable_streams": ["Any stream + Design college"],
            "required_strengths": ["Creativity", "Visual thinking"],
            "interest_areas": ["design", "creativity", "technology"],
        },
        {
            "title": "Teacher / Educator",
            "emoji": "📚",
            "description": "Teach, guide, and inspire the next generation.",
            "suitable_streams": ["Arts", "Science", "Commerce"],
            "required_strengths": ["Patience", "Communication"],
            "interest_areas": ["teaching", "helping"],
        },
    ]
    for c in careers:
        db.add(CareerOption(**c))
    print("✓ Career options seeded")


def seed_pricing(db):
    plans = [
        {
            "name": "Assessment Only",
            "emoji": "📋",
            "price": "₹999",
            "tagline": "Get your psychometric report",
            "description": "Take the full psychometric assessment and receive a detailed written report.",
            "includes": ["Full psychometric assessment", "Personalised written report", "Career recommendations", "Email delivery within 48 hrs"],
            "suitable_for": "Students who want a starting point",
            "is_highlighted": False,
            "order_index": 1,
        },
        {
            "name": "Assessment + Report Session",
            "emoji": "📊",
            "price": "₹1,799",
            "original_price": "₹2,200",
            "tagline": "Report + one session to understand it",
            "description": "The full assessment plus a 30-minute session to walk through results.",
            "includes": ["Full assessment", "Personalised report", "30-min result review", "WhatsApp follow-up 7 days"],
            "suitable_for": "Students who want to understand their results",
            "is_highlighted": False,
            "order_index": 2,
        },
        {
            "name": "Assessment + Full Mentoring",
            "emoji": "🎯",
            "price": "₹3,499",
            "original_price": "₹4,500",
            "tagline": "Most popular — complete guidance",
            "description": "Full assessment + 60-min mentoring + career action plan.",
            "includes": ["Full assessment", "Detailed report", "60-min mentoring", "Career action plan", "WhatsApp 30 days", "Free check-in after 30 days"],
            "suitable_for": "Students serious about finding their direction",
            "is_highlighted": True,
            "badge": "Most Popular",
            "order_index": 3,
        },
        {
            "name": "Premium Package",
            "emoji": "🌟",
            "price": "₹5,999",
            "original_price": "₹8,000",
            "tagline": "Deep guidance over 3 months",
            "description": "Comprehensive support including multiple sessions and 3-month follow-up.",
            "includes": ["Full assessment", "3 mentoring sessions", "1-3 year roadmap", "College shortlisting", "Parent session", "3 months WhatsApp"],
            "suitable_for": "Students who want maximum support",
            "is_highlighted": False,
            "badge": "Best Value",
            "order_index": 4,
        },
        {
            "name": "Parent Counselling Session",
            "emoji": "👨‍👩‍👧",
            "price": "₹1,299",
            "tagline": "For parents of confused students",
            "description": "45-minute session for parents to understand results and support their child.",
            "includes": ["45-min parent session", "Understanding the report", "How to support without pressure", "WhatsApp follow-up"],
            "suitable_for": "Parents — student assessment required",
            "is_highlighted": False,
            "order_index": 5,
        },
        {
            "name": "College Guidance Session",
            "emoji": "🏫",
            "price": "₹1,999",
            "tagline": "Find the right college",
            "description": "Focused session on college shortlisting based on your profile and goals.",
            "includes": ["45-60 min session", "College shortlist", "Course guidance", "Written summary", "WhatsApp Q&A 14 days"],
            "suitable_for": "Class 12 / first-year college students",
            "is_highlighted": False,
            "order_index": 6,
        },
    ]
    for p in plans:
        db.add(PricingPlan(**p))
    print("✓ Pricing plans seeded")


def run():
    print("🌱 Starting database seed...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Testimonial).delete()
        db.query(FAQ).delete()
        db.query(CareerOption).delete()
        db.query(PricingPlan).delete()
        db.commit()

        seed_testimonials(db)
        seed_faqs(db)
        seed_careers(db)
        seed_pricing(db)
        db.commit()
        print("✅ Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()
