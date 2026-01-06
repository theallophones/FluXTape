# FluXTape

**Songs as Probability Clouds**

FluXTape reimagines music streaming by treating songs as dynamic, collaborative spaces where multiple versions coexist. Artists release stems with alternate arrangements, contributors create new versions, and listeners explore different combinations rather than hearing a single fixed recording.

---

## Core Concept

Traditional streaming platforms lock songs into a single "final" mix. FluXTape breaks this constraint by allowing:

- **Artists** to release multiple versions of lyrics, grooves, solos, and spatial mixes
- **Contributors** to remix stems and submit new arrangements
- **Listeners** to explore alternate versions, with playback influenced by community rankings

Every play can reveal a different combination. The song stays fluid, and the boundaries between creator and audience become more flexible.

---

## Platform Components

This project consists of three interconnected prototypes:

### 1. Artist Dashboard
Upload stems organized by song sections and features. Define creative constraints and set contributor periods.

**Repository**: [FluXTape-Artist_Dashboard](https://github.com/theallophones/FluXTape-Artist_Dashboard)  
**Live Demo**: https://fluxtape-artistdashboard-1.streamlit.app/

### 2. Contributor Studio
Real-time stem manipulation interface. Mix alternate versions, adjust individual volumes, and create new arrangements.

**Repository**: [FluXTape_Subscribers](https://github.com/theallophones/FluXTape_Subscribers)  
**Live Demo**: https://fluxtape-nvnvxr6b38tettxyxngaeu.streamlit.app/

### 3. Listener Stream
Free streaming interface exploring version selection and community engagement with alternate arrangements.

**Repository**: [FluXTape_Streaming](https://github.com/theallophones/FluXTape_Streaming)  
**Live Demo**: https://fluxtape-streaming-1.streamlit.app/

---

## Research Questions

FluXTape also serves as a research platform investigating:

- Do listeners consistently prefer certain lyrical/instrumental combinations?
- Is there a "best version" for most people, or does preference vary widely?
- How does familiarity influence version selection?
- Can these patterns inform songwriting and production practices?

This builds on empirical work examining emotional interactions between lyrics and music.

---

## Technical Stack

- **Frontend**: Streamlit (rapid prototyping)
- **Audio Processing**: Web Audio API, WaveSurfer.js
- **Deployment**: Streamlit Cloud
- **Audio Hosting**: GitHub raw content delivery

---

## Repository Structure
```
FluXTape/
├── archive/           # Early prototypes and development history
├── README.md          # This file
└── requirements.txt   # Python dependencies
```

Individual interface code lives in the linked repositories above.

---

## Current Status

**Stage**: Early prototype / exploratory validation

All three interfaces are functional prototypes demonstrating core concepts. Current work focuses on:
- Validating user interest and engagement patterns
- Refining the version selection algorithm
- Exploring contributor incentive models
- Planning pilot studies with independent artists

---

## About

Built by [Peyman Salimi](https://peymansalimi.com) at Georgia Tech as an independent student project.

**Contact**: peymansalimi@gatech.edu

---

## License

MIT License - see individual repositories for details.

---

*Last updated: January 2026*
