# (geo)osint - 498 pts

> **Category:** OSINT
> **Difficulty:** Medium-Hard
> **Solves:** 8 teams
> **Status:** ✅ Solved

---

## Challenge Description

> *Answer the following questions about geo(?)osint.*

**Attachments:** 5 images (osint_1.jpg through osint_5.png)
**Instance:** `nc public.ctf.r0devnull.team 3016`

---

## Challenge Format

Multi-question OSINT quiz with 5 geolocation challenges. Each answer unlocks the next question.

---

## Solutions

### Q1: Building Name (osint_1.jpg)

> *Could u name the name of the building?*
> Format: case sensitive, replace spaces with `_`

**Image:** Interior shot of ornate conference hall with chandeliers

**Answer:** `Palace_of_Parliament`

**Method:** Recognized the grand interior of Romania's Palace of Parliament (Palatul Parlamentului) in Bucharest. The baroque-style ceiling and conference setup matched known photos of events held there.

---

### Q2: Lamborghini Address (osint_2.jpg)

> *Could u name the address where I found this versace lamborghini?*
> Format: `street street_number, city postal_code`

**Image:** White Lamborghini at night in parking lot, gas station visible

**Answer:** `Calea Craiovei 127, Pitești 110207`

**Method:**
1. License plate showed **AG** (Argeș county, Romania) - main city is Pitești
2. Reverse image search found owner's social media in "Pitesti Centru"
3. Matched background buildings to locate exact address

---

### Q3: Building Near Area (osint_3.jpg)

> *Could u name the name of the building near this area?*

**Image:** Soviet-era apartment blocks, street view

**Answer:** `Politehnica_Business_Tower`

**Method:**
1. License plate showed **B** (Bucharest)
2. Located area using Superbet/Fortuna betting shops as landmarks
3. Identified nearby notable building

---

### Q4: Building Near Area (osint_4.jpg)

> *Could u name the name of the building near this area?*

**Image:** Parking lot at night with covered structure

**Answer:** `Gara_Pitesti`

**Method:**
1. License plates showed **AG** (Argeș county)
2. Parking structure matched train station style
3. Confirmed via Google Street View at Bulevardul Republicii 212, Pitești
4. Note: Romanian diacritics (ș, ț) not needed - `Gara_Pitesti` accepted

---

### Q5: ISS Coordinates (osint_5.png)

> *I want the coordinates from this place with the precision of 7 decimals!*
> Format: `coord1,coord2`

**Image:** Interior of International Space Station with mission patches

**Answer:** `29.5604361,-95.0853103`

**Method:**
1. Recognized ISS interior from mission patches and equipment
2. Google has "Street View" imagery of the ISS
3. Google geotagged ISS imagery to **NASA Johnson Space Center** coordinates (Houston, TX)
4. Extracted coordinates directly from Google Maps Street View metadata

---

## Flag

```
nullctf{pl34s3_d0_n07_d0x_m3!}
```

---

## Lessons Learned

| Lesson | Details |
|--------|---------|
| Romanian license plates | County codes: B=Bucharest, AG=Argeș, SB=Sibiu, etc. |
| Reverse image search | Essential for finding original sources with metadata |
| Google Street View metadata | Even "virtual" locations (ISS) have geotagged coordinates |
| Betting shop chains | Superbet/Fortuna can serve as landmarks for Eastern European geolocation |
| Diacritics | Romanian characters (ș, ț, ă, î) may or may not be required - try both |

---

## Tools Used

- Google Maps / Street View
- Google Images (reverse image search)
- exiftool (EXIF metadata extraction)
- License plate lookups (Romanian county codes)

---

## Resources

- [Romanian License Plate Codes](https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_Romania)
- [Google ISS Street View](https://www.google.com/streetview/)
- [NASA Image Archive](https://images.nasa.gov/)

---

## Files

| File | Description |
|------|-------------|
| [files/osint_1.jpg](files/osint_1.jpg) | Palace of Parliament interior |
| [files/osint_2.jpg](files/osint_2.jpg) | Lamborghini in Pitești |
| [files/osint_3.jpg](files/osint_3.jpg) | Bucharest street view |
| [files/osint_4.jpg](files/osint_4.jpg) | Gara Pitești parking |
| [files/osint_5.png](files/osint_5.png) | ISS interior |

---

*Tags: #nullctf2025 #osint #geolocation #romania #iss*
