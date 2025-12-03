# Project Codex - Presentation Script (2 People)

**Presenters:** Rimpa & Chay
**Duration:** 10-12 minutes
**Format:** Rimpa presents first half, Chay presents second half + demo

---

## PART 1: RIMPA'S SECTION (5-6 minutes)

### Opening & Introduction (30 seconds)

Good [morning/afternoon] everyone! My name is Rimpa, and together with my partner Chay, we're from the Middleware Team. Today we're excited to present **Project Codex** - a medicine name translation system that helps users find equivalent medications across different countries.

Before I dive in, let me ask you something: Imagine you're traveling from the US to India and you have a terrible headache. You usually take Tylenol, but when you get to the pharmacy in Mumbai, they've never heard of it. You try to explain - "acetaminophen?" - still nothing. You need relief, but you don't know what to ask for. This exact scenario happens to millions of travelers every year, and that's the problem Project Codex solves.

---

### Problem Statement (1 minute)

The challenge we're addressing is both simple and critical - the same medication often has completely different brand names in different countries, even when the active ingredient is identical.

Let me give you some examples:
- **Pain Relief:** In the US, you take Tylenol for a headache. In India, the equivalent is Dolo 650 or Calpol. In the UK and Australia, it's called Panadol. All of these are the exact same drug - paracetamol or acetaminophen - just different brand names.

- **Anti-inflammatory:** If you use Advil or Motrin in the US, you'd ask for Brufen or Combiflam in India, or Nurofen in the UK and Australia. Same ibuprofen, different names.

- **Cholesterol medication:** Lipitor in the US becomes Atocor in India, or generic Atorvastatin in the UK.

And this isn't just about pain relievers or common medications. This applies to cholesterol medications, acid reflux treatments, allergy medicines, blood pressure medications - essentially any over-the-counter or prescription drug.

The consequences of not knowing this information can range from inconvenient to dangerous. You might:
- Pay for an unnecessary doctor's visit just to get a medication name
- Take the wrong medication because of confusion
- Go without needed medication
- Face language barriers that complicate the situation further

Our system, Project Codex, bridges this gap.

---

### Solution Overview (45 seconds)

Project Codex is a full-stack web application that allows users to:
1. Enter a medication name from their home country
2. Select which country they're traveling to or currently in
3. Instantly receive a list of equivalent medications available in that country, complete with both brand names and generic active ingredients

The system currently supports five major regions: United States, India, United Kingdom, Canada, and Australia, and covers multiple medication categories including pain relief, anti-inflammatory, antihistamines, cholesterol medications, and acid reflux treatments.

But what makes our project unique isn't just what it does - it's how it's built.

---

### Architecture Overview (2 minutes)

As the middleware team, our role was crucial - we built the orchestration layer that coordinates multiple independent services. Let me walk you through our architecture.

*[Pause for any visual/diagram if available]*

Our system consists of four main components:

**1. React Frontend**
- Clean, user-friendly interface
- Simple form with medication name input and country dropdowns
- Displays results in an easy-to-read card format
- Built with React and Vite for fast performance

**2. FastAPI Middleware - The Backbone**
- This is our main contribution - the `main.py` file
- Acts as the orchestrator coordinating all services
- Handles all validation and error handling
- Manages the entire request/response lifecycle
- Built with FastAPI for high performance and automatic API documentation

**3. Translation Service**
- Handles language and region-specific translations
- Validates that the language pair is supported
- In our current implementation, it handles regional naming conventions

**4. Database Lookup Service**
- Contains comprehensive medication mappings
- Searches based on active ingredients
- Returns all available brands for the requested country
- Based on verified medical data

Now here's the key innovation: **JSON-based inter-service communication**.

Instead of tightly coupling these services with direct API calls or complex message queues, our middleware communicates with the other services through JSON files. Here's how it works:

- The middleware receives a request and writes a `translation_input.json` file
- The Translation Service watches for this file, processes it, and writes `translation_output.json`
- The middleware reads that output and writes `lookup_input.json`
- The Database Service detects this file, processes it, and writes `lookup_output.json`
- The middleware reads the final results and sends them back to the frontend

This architecture provides several advantages:
- **Loose Coupling:** Each service is completely independent
- **Parallel Development:** Different teams can work simultaneously without blocking each other
- **Language Agnostic:** Services can be written in any programming language as long as they follow the JSON contract
- **Easy Debugging:** You can literally open the JSON files and see exactly what data is being passed
- **Simple Testing:** You can manually create JSON files to test individual services
- **No Infrastructure Overhead:** No need to set up and maintain message brokers or complex service meshes

---

### Real-World Applications (1 minute)

While this is a capstone demonstration, the real-world applications are significant and impactful:

**For International Travelers:**
- Quick medication lookup when abroad
- Avoid language barriers at foreign pharmacies
- Ensure you're getting the correct active ingredient
- Peace of mind when dealing with health issues away from home

**For Healthcare Providers:**
- Assist international patients who are taking medications from their home countries
- Verify medication equivalents when treating tourists or immigrants
- Support telemedicine consultations across borders
- Reduce medication errors due to naming confusion

**For Pharmacists:**
- Help customers find local equivalents for foreign prescriptions
- Verify generic compositions quickly
- Provide better customer service to international visitors
- Reduce the time spent researching unfamiliar medication names

**For Immigrants and Expatriates:**
- Continue medication regimens when moving countries
- Understand prescriptions from doctors in new countries
- Communicate medication histories to new healthcare providers

This isn't just a technical exercise - it's a solution to a real problem that affects millions of people every year.

---

### Database Coverage (30 seconds)

Our current database is comprehensive within its scope. We support:

**Five Countries:**
- United States
- India
- United Kingdom
- Canada
- Australia

**Multiple Medication Categories:**
- **Pain and Fever Relief:** Tylenol, Panadol, Dolo 650, Calpol
- **Anti-inflammatory (NSAIDs):** Advil, Motrin, Nurofen, Brufen, Combiflam
- **Antihistamines:** Benadryl, Nytol, Boots Sleepeaze, Restavit
- **Cholesterol Medications:** Lipitor, Atocor, generic Atorvastatin
- **Acid Reflux (Proton Pump Inhibitors):** Prilosec, Nexium, Omez, Ocid, Losec

Each medication entry includes:
- Brand name (what you ask for at the pharmacy)
- Generic name (the active ingredient)
- Typical dosage information

And the system is designed to be easily extensible - adding new medications or countries is straightforward.

---

### Handoff to Chay

Now I'd like to hand it over to my partner Chay, who will dive deep into the technical implementation, walk you through our middleware code, demonstrate the system live, and discuss the challenges we overcame during development.

Chay, take it away.

---

## PART 2: CHAY'S SECTION (5-6 minutes)

### Introduction to Technical Section (15 seconds)

Thanks Rimpa!

Now let's get into the technical details - how we actually built this system, how the middleware orchestrates everything, and most importantly, let's see it working live.

---

### Middleware Technical Deep Dive (2 minutes)

Let me walk you through our middleware implementation - the `main.py` file that serves as the backbone of Project Codex.

**Technology Choice:**
We used FastAPI, a modern Python web framework, because it provides:
- Automatic API documentation
- Built-in data validation with Pydantic
- High performance (comparable to Node.js and Go)
- Type hints for better code quality
- Async support for handling concurrent requests

**The Request Flow:**

When a user makes a request, here's exactly what happens in our middleware:

**Step 1: Input Validation**
```python
class UserInput(BaseModel):
    original_language: str
    requested_language: str
    original_medication: str
```

We receive three required fields and validate that:
- None of the fields are empty
- All strings are properly stripped of whitespace
- The data types are correct

If validation fails, we immediately return a 400 Bad Request error with a clear message.

**Step 2: Translation Phase**
```python
translation_input = {
    "original_language": data.original_language.strip(),
    "requested_language": data.requested_language.strip(),
    "original_medication": data.original_medication.strip()
}
write_json(TRANSLATION_INPUT, translation_input)
```

We format the data into our standard JSON structure and write it to `translation_input.json`.

Then we wait - using a helper function that polls for the existence of `translation_output.json` with a 10-second timeout. This prevents indefinite hanging if the translation service crashes or is slow.

When the translation output arrives, we validate:
- Is the language pair supported?
- Did we get a translated medication name back?

If either check fails, we return an appropriate error.

**Step 3: Database Lookup Phase**
```python
cleaned_translation = {
    "translated_medication": translated_medication.strip(),
    "requested_language": data.requested_language,
    "original_medication": data.original_medication,
}
write_json(BACKEND_INPUT, cleaned_translation)
```

We take the translated medication name and write it to `lookup_input.json` for the database service.

Again, we wait for `lookup_output.json` with timeout protection.

When the lookup results arrive, we validate:
- Did the lookup succeed?
- Do we have actual medication matches?

**Step 4: Response Formatting**
```python
final_matches = [
    {
        "generic": m.get("generic"),
        "brand": m.get("brand")
    }
    for m in matches
]

return {
    "original_language": data.original_language,
    "requested_language": data.requested_language,
    "original_medication": data.original_medication,
    "translated_medication": translated_medication,
    "medication_matches": final_matches
}
```

We clean up the data, format it consistently, and return it to the frontend.

**Error Handling at Every Step:**

We implemented comprehensive error handling:
- **400 Errors:** Invalid input, unsupported languages
- **404 Errors:** No medications found in the database
- **500 Errors:** Service timeouts, missing data from services
- **CORS Middleware:** Allows our React frontend to communicate with the backend

Every error returns a clear, actionable message to the user.

---

### Supporting Services (1 minute)

To make this work end-to-end, I also implemented two supporting services:

**Translation Service (`translation_service.py`):**
- Uses Python's Watchdog library to monitor the file system
- Detects when `translation_input.json` is created or modified
- Validates the language pair against our supported countries
- For our demo, since all countries use English brand names, it passes the medication name through
- In production, this would interface with translation APIs or medical terminology databases
- Writes `translation_output.json` with the result

**Database Lookup Service (`database_service.py`):**
- Also uses Watchdog for file system monitoring
- Contains a comprehensive dictionary of medication mappings
- When it detects `lookup_input.json`, it:
  - Converts the medication name to lowercase for case-insensitive matching
  - Looks up the medication in its database
  - Finds all available brands in the requested country
  - Returns them with both generic and brand names
- Writes `lookup_output.json` with all matches

The database is populated from the information in `medicines.txt`, which contains real medication mappings based on active ingredients.

**File System Watching:**
Both services use the Watchdog library's Observer pattern:
```python
observer = Observer()
observer.schedule(event_handler, path=".", recursive=False)
observer.start()
```

This provides real-time response when JSON files are created - much more efficient than polling.

---

### Live Demo (2 minutes)

Alright, let's see this in action!

*[Share screen showing http://localhost:3000]*

Here's our frontend interface - clean and straightforward. You have:
- A text input for the medication name
- A dropdown to select the origin country
- A dropdown to select the destination country
- A search button

Let's start with a common scenario. I'm traveling from the US to India and I need my regular pain medication.

*[Type and demonstrate]*
- Medicine: **Tylenol**
- From: **US**
- To: **India**
- Click **Search**

*[While it's processing, quickly switch to terminal]*

Look at our backend terminal - see the services lighting up:
- Translation Service detected the input and processed it
- Database Service picked up the lookup request
- All coordinated by our FastAPI middleware

*[Switch back to browser]*

And here are our results! In India, instead of asking for Tylenol, you want:
- **Dolo 650** - Paracetamol 650mg
- **Calpol 650** - Paracetamol 650mg

Both are the exact same active ingredient - paracetamol - just different brands. You can walk into any pharmacy in India and ask for either of these.

Let's try another example - anti-inflammatory medication from the US to the UK.

*[New search]*
- Medicine: **Advil**
- From: **US**
- To: **UK**
- Click **Search**

Result: **Nurofen** - same ibuprofen, different brand. This is what you'd find in any UK pharmacy or supermarket.

One more - cholesterol medication, which is especially important for people managing chronic conditions.

*[New search]*
- Medicine: **Lipitor**
- From: **US**
- To: **India**
- Click **Search**

Result: **Atocor** - both are atorvastatin. For someone managing their cholesterol while traveling or relocating, this information could be critical.

The system works both ways too. Let me search for an Indian medication to find its US equivalent.

*[New search]*
- Medicine: **Dolo 650**
- From: **India**
- To: **US**
- Click **Search**

And we get **Tylenol** - perfect reverse lookup.

All of this happens in under a second, with three separate services coordinating through our middleware.

---

### Challenges & Solutions (1.5 minutes)

During development, we faced several interesting challenges:

**Challenge 1: File System Timing Issues**

Initially, we tried simple polling - checking every second if the JSON file existed. The problem was:
- Too slow: 1-second delays felt sluggish to users
- Too fast: Polling every 100ms wasted CPU cycles
- Race conditions: Sometimes we'd read the file before it was fully written

**Solution:** We implemented the Watchdog library which uses OS-level file system events. It detects file creation or modification instantly and reliably, with no polling overhead.

**Challenge 2: CORS Errors**

When we first connected the React frontend to the FastAPI backend, requests were failing with CORS errors. The browser was blocking requests from localhost:3000 (frontend) to localhost:8000 (backend) because they're different origins.

**Solution:** We added CORS middleware to FastAPI:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This explicitly allows our frontend to communicate with the backend while maintaining security.

**Challenge 3: Service Coordination**

What happens if:
- The translation service crashes?
- The database service is slow?
- A JSON file is corrupted?

**Solution:** We implemented multiple safeguards:
- Timeout protection (10 seconds max per service)
- Try-catch blocks around all file operations
- Validation at every step
- Clear error messages propagated back to the user
- Graceful degradation - the system doesn't crash, it reports the error

**Challenge 4: Case-Insensitive Medication Lookup**

Users might type "tylenol", "Tylenol", or "TYLENOL". We needed consistent matching.

**Solution:** In the database service, we convert all medication names to lowercase before lookup:
```python
translated_med = data.get("translated_medication", "").lower().strip()
```

This ensures reliable matching regardless of how the user types the medication name.

**Challenge 5: Data Accuracy**

Medical data is sensitive - wrong information could be dangerous.

**Solution:**
- Based our database on verified sources (medicines.txt from medical references)
- Always include the generic name (active ingredient) with the brand name
- In a production system, we'd partner with medical databases like RxNorm
- Include disclaimers that users should consult healthcare professionals

---

### Technical Stack Summary (30 seconds)

To summarize our technology choices:

**Backend:**
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Watchdog** - File system monitoring
- **Uvicorn** - ASGI server

**Frontend:**
- **React** - UI framework
- **Vite** - Build tool for fast development
- **Axios** - HTTP client

**Architecture:**
- **JSON-based messaging** - Inter-service communication
- **RESTful API** - Frontend-backend communication
- **File system events** - Service coordination

**Development Tools:**
- **Git** - Version control
- **Virtual environments** - Python dependency isolation
- **npm** - JavaScript package management

---

### Future Enhancements (45 seconds)

Looking ahead, here's how we could expand Project Codex:

**Immediate Enhancements:**
- Add more countries - Japan, Germany, France, Brazil, China
- Expand medication database - thousands more medications
- Include dosage conversion (500mg vs 650mg equivalents)
- Add drug interaction warnings

**Medium-term Features:**
- Mobile app version for iOS and Android
- OCR capability to scan medication bottles
- User accounts to save medication lists
- Integration with pharmacy inventory systems
- Offline mode with local database

**Advanced Features:**
- AI-powered medication recognition from photos
- Multi-language support for the interface itself
- Telemedicine platform integration
- Prescription upload and analysis
- User reviews and ratings for medication availability
- Push notifications for medication recalls or updates

**Production Readiness:**
- Migration from file-based to message queue (RabbitMQ or Kafka)
- Database migration from dictionary to PostgreSQL
- Request ID tracking for concurrent requests
- Comprehensive logging and monitoring
- Load balancing and horizontal scaling
- Automated testing and CI/CD pipeline

---

### Code Quality & Repository (30 seconds)

We took code quality seriously throughout this project:

**Documentation:**
- Comprehensive README with setup instructions
- Step-by-step guide to run the application
- Troubleshooting section for common issues
- API documentation auto-generated by FastAPI

**Code Organization:**
- Clear separation of concerns between services
- Type hints throughout Python code
- Consistent naming conventions
- Proper error handling at every level

**Deployment:**
- `requirements.txt` for Python dependencies
- `package.json` for frontend dependencies
- `start_backend.sh` script to launch all services with one command
- `.gitignore` to exclude generated files and dependencies

**Best Practices:**
- Virtual environment for Python isolation
- No hardcoded secrets or credentials
- CORS properly configured
- Input validation and sanitization

Everything is in our GitHub repository with full documentation, so other developers can easily understand, run, and extend our work.

---

### Closing (30 seconds)

To wrap up, Project Codex demonstrates:

1. **Effective middleware architecture** using JSON-based communication that's simple, debuggable, and flexible

2. **Clean separation of concerns** - frontend, middleware, and backend services all work independently

3. **Real-world application** solving a genuine problem for millions of international travelers, healthcare providers, and expatriates

4. **Scalable design** that can easily be extended with more countries, medications, and features

5. **Production-ready code** with proper error handling, validation, and documentation

We're proud of what we built, and we believe this architecture pattern - using lightweight JSON-based messaging coordinated by a robust middleware layer - could be applied to many other scenarios beyond medication translation.

The middleware approach we demonstrated here shows how different teams can work independently while still delivering a cohesive, functional application.

Thank you for your time! We're happy to answer any questions you might have.

---

## Q&A PREPARATION - ANSWERS FOR BOTH PRESENTERS

**Q: Why use JSON files instead of a message queue like RabbitMQ or Kafka?**

**Answer (Either presenter):** Great question! For our use case and capstone project:
- **Simplicity:** JSON files are incredibly easy to debug - you can literally open and read them to see exactly what's being passed
- **No Infrastructure:** No need to set up, configure, and maintain a message broker
- **Learning Objectives:** Perfect for demonstrating middleware concepts without infrastructure complexity
- **Development Speed:** Much faster to prototype and test

That said, for a production environment with high traffic and concurrent requests, we would absolutely migrate to RabbitMQ, Kafka, or Redis Pub/Sub. Those systems provide message queuing, delivery guarantees, and scalability that file-based systems can't match. But for our capstone demo, JSON files strike the perfect balance between simplicity and functionality.

---

**Q: How do you handle concurrent requests? What if two users search at the same time?**

**Answer (Chay preferred):** Currently, our demo processes requests sequentially. Each request creates and overwrites the same JSON files, so concurrent requests would interfere with each other.

For production, we'd implement:
- **Unique request IDs** in filenames (e.g., `translation_input_<uuid>.json`)
- **Message queues** that naturally handle concurrency
- **Database-backed queue** to track request status
- **API-based communication** instead of file-based for real-time handling
- **Horizontal scaling** with multiple worker instances

This is one of the main reasons we'd migrate to a message queue system for production - they're built to handle concurrent requests elegantly.

---

**Q: What about medication dosages? They vary by country.**

**Answer (Rimpa preferred):** Excellent point! You're absolutely right - Tylenol in the US might be 500mg tablets while Dolo in India comes in 650mg tablets.

Our current implementation includes dosage information in the generic name field (like "Paracetamol 650mg"), so users can see the dosage differences.

For a production system, we would:
- Add dedicated dosage fields with min/max ranges
- Implement dosage conversion algorithms
- Include prominent warnings when dosages differ significantly
- Possibly consult with pharmacists to provide dosage recommendations
- Require user acknowledgment for dosage variations
- Link to official medical guidelines for each medication

Medical dosing is critical, so we'd never want users to assume exact equivalence without understanding dosage differences.

---

**Q: How accurate is your medication database? Where did you get the data?**

**Answer (Rimpa preferred):** Our database is based on research compiled in our `medicines.txt` file, which includes verified medication mappings based on active ingredients from medical references.

However, we want to be absolutely clear: **this is a demonstration system**. For real-world deployment, we would:
- Partner with established medical databases like RxNorm, DrugBank, or WHO INN
- Employ licensed pharmacists as consultants to verify all mappings
- Implement a rigorous review and update process
- Add "last verified" timestamps to all data
- Include legal disclaimers throughout the interface
- Require users to consult healthcare professionals before making medication decisions

We would never recommend someone rely solely on any automated system for medical decisions without professional healthcare consultation. This tool should augment, not replace, medical advice.

---

**Q: Can this handle prescription medications?**

**Answer (Chay preferred):** Currently, we focus on common over-the-counter medications to demonstrate the concept. Prescription drugs add significant complexity:
- **Legal restrictions** vary dramatically by country
- **Controlled substances** have special regulations
- **Dosage calculations** become more critical
- **Availability** - some medications simply aren't available in certain countries
- **Liability concerns** - wrong information could be dangerous

Architecturally, yes - the system could absolutely be extended to include prescription medications. But we'd need:
- Partnerships with medical authorities
- Licensed pharmacist oversight
- Legal compliance frameworks for each country
- Enhanced verification processes
- Stricter data validation
- Professional medical review of all data

It's technically feasible but would require significant domain expertise and legal oversight.

---

**Q: What happens if one of the services goes down?**

**Answer (Chay preferred):** We have timeout protection - after 10 seconds, the middleware will timeout and return a clear error message to the user explaining that the service is unavailable.

For production resilience, we'd implement:
- **Health check endpoints** for all services
- **Automatic retry logic** with exponential backoff
- **Circuit breaker pattern** to prevent cascade failures
- **Fallback mechanisms** - maybe cached results for common queries
- **Service monitoring** with tools like Prometheus or DataDog
- **Alerting** to notify developers of service failures
- **Redundancy** - multiple instances of each service behind a load balancer

The goal would be to maintain availability even if individual service instances fail.

---

**Q: Why did you choose React for the frontend instead of Vue, Angular, or vanilla JavaScript?**

**Answer (Either presenter):** We chose React for several reasons:
- **Industry standard** - React is the most widely used frontend framework, making our project relevant to real-world development
- **Component-based architecture** - Easy to maintain and extend
- **Great ecosystem** - Tons of libraries and community support
- **Developer experience** - Paired with Vite, we get hot module replacement and instant feedback
- **Team familiarity** - We're comfortable with React from other projects

We also considered:
- **Vue** - Great choice, but React has more industry adoption
- **Angular** - More opinionated and heavier, overkill for our use case
- **Vanilla JS** - Would work, but we'd end up reinventing component patterns

React + Vite gave us the fastest development experience while maintaining professional standards.

---

**Q: How would you secure this for production use?**

**Answer (Chay preferred):** Security would be a top priority for production deployment:

**Authentication & Authorization:**
- User registration and login system
- JWT tokens for session management
- Role-based access control (regular users, pharmacists, administrators)
- OAuth integration for social login

**Network Security:**
- HTTPS everywhere with valid SSL certificates
- CORS properly configured for specific domains
- Rate limiting to prevent abuse (e.g., max 10 requests per minute per user)
- API gateway for request filtering

**Data Security:**
- Input sanitization to prevent injection attacks
- SQL parameterization (when we migrate to a database)
- No sensitive data in JSON files
- Encryption at rest for any stored user data

**Monitoring & Compliance:**
- Comprehensive audit logging of all requests
- GDPR compliance for European users
- HIPAA consideration for US healthcare data
- Regular security audits and penetration testing
- Dependency scanning for vulnerabilities

**Infrastructure:**
- Services running in isolated containers
- Secrets management (not hardcoded credentials)
- Automated security patches
- Firewall rules limiting service-to-service communication

---

**Q: Can you show me the API documentation?**

**Answer (Chay preferred):** Absolutely! One of the benefits of FastAPI is that it automatically generates interactive API documentation.

*[Navigate to http://localhost:8000/docs]*

Here you can see:
- The `/process` endpoint with full request and response schemas
- Try it out directly from the browser
- See all validation rules
- Check response codes and error messages

There's also an alternative documentation view at `/redoc` if you prefer a cleaner, more readable format.

This documentation is always in sync with the code because it's generated from our Pydantic models and type hints.

---

**Q: What was the most difficult part of this project?**

**Answer (Either presenter, personal reflection):**

**Chay might say:** The most challenging part was coordinating the timing between services. Getting the file watching to work reliably without race conditions took several iterations. We had to balance between reading files too quickly (before they were fully written) and waiting too long (poor user experience). The Watchdog library solved this elegantly, but it required careful event handler implementation.

**Rimpa might say:** For me, it was ensuring data accuracy in the medication database. Medical information is sensitive - we can't just guess at equivalents. Every mapping had to be verified based on active ingredients, and we had to be careful about how we present the information to make clear these are equivalents based on ingredients, not exact substitutes. The responsibility of providing health-related information, even in a demo, weighed on me.

---

**Q: How long did this project take to build?**

**Answer (Either presenter):** From concept to working demo, we spent approximately [X weeks/days - adjust to reality]:
- **Planning & Architecture:** [Y time] - designing the middleware approach, defining JSON contracts
- **Backend Development:** [Y time] - implementing the FastAPI middleware and supporting services
- **Frontend Development:** [Y time] - building the React interface
- **Database Population:** [Y time] - researching and verifying medication mappings
- **Integration & Testing:** [Y time] - connecting all pieces and fixing bugs
- **Documentation:** [Y time] - README, setup instructions, this presentation

The modular architecture actually sped up development because we could work on services independently and test them in isolation before integrating.

---

## PRESENTATION TIPS

### For Rimpa (Part 1):
- **Energy:** Start strong - you're setting the tone for the entire presentation
- **Pacing:** Speak clearly and not too fast, especially during the problem statement
- **Audience Connection:** Make eye contact when describing the traveler scenario - make it relatable
- **Transitions:** Clearly signal when you're moving from problem → solution → architecture
- **Handoff:** Give Chay a strong setup - "Now let's see how we built this technically"

### For Chay (Part 2):
- **Technical Clarity:** Don't assume everyone knows FastAPI or React - briefly explain
- **Demo Confidence:** Practice the demo multiple times so you can do it smoothly
- **Backup Plan:** Have screenshots ready in case the demo fails
- **Enthusiasm:** Show excitement about the technical solutions
- **Closing Strength:** End on a high note - this is what the audience remembers

### Both:
- **Practice Together:** Run through the handoff multiple times
- **Time Management:** Use a timer during practice - stick to your sections
- **Questions:** Decide beforehand who answers which types of questions
- **Support Each Other:** If one person gets stuck, the other can jump in naturally
- **Professional But Personable:** You're demonstrating competence, but also show personality

---

## PRE-PRESENTATION CHECKLIST

### 24 Hours Before:
- [ ] Full run-through together, timed
- [ ] Test all services on presentation laptop
- [ ] Prepare backup slides/screenshots
- [ ] Charge laptop fully
- [ ] Test display connection if in-person

### 1 Hour Before:
- [ ] Start all backend services
- [ ] Start frontend and verify it works
- [ ] Test 3-4 medication searches
- [ ] Close unnecessary applications
- [ ] Turn off notifications (Slack, email, etc.)
- [ ] Clear browser history if needed
- [ ] Set browser zoom to 125-150% for visibility
- [ ] Have terminal and browser windows positioned
- [ ] Water bottles ready

### 5 Minutes Before:
- [ ] Deep breath!
- [ ] One final test search
- [ ] Terminal ready but in background
- [ ] Browser at localhost:3000
- [ ] Smile - you've built something great!

---

## TIMING BREAKDOWN

**Rimpa's Section: 5-6 minutes**
- Opening: 0:00-0:30
- Problem Statement: 0:30-1:30
- Solution Overview: 1:30-2:15
- Architecture: 2:15-4:15
- Real-World Applications: 4:15-5:15
- Database Coverage: 5:15-5:45
- Handoff: 5:45-6:00

**Chay's Section: 5-6 minutes**
- Technical Introduction: 6:00-6:15
- Middleware Deep Dive: 6:15-8:15
- Supporting Services: 8:15-9:15
- Live Demo: 9:15-11:15
- Challenges: 11:15-12:45
- Technical Stack: 12:45-13:15
- Future Enhancements: 13:15-14:00
- Code Quality: 14:00-14:30
- Closing: 14:30-15:00

**Q&A: 15:00+**

**Total: 12-15 minutes + Q&A**

---

Good luck! You've built something genuinely useful and technically sound. Present with confidence! 🚀
