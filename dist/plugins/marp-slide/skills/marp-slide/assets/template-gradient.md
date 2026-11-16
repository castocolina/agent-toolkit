---
marp: true
theme: default
paginate: true
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');

:root {
  --color-foreground: #ffffff;
  --color-heading: #ffffff;
  --color-accent: #ffd700;
  --font-default: 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif;
}

section {
  background: linear-gradient(135deg, #3b3f9e 0%, #6a2c91 50%, #a3286f 100%);
  color: var(--color-foreground);
  font-family: var(--font-default);
  font-weight: 400;
  box-sizing: border-box;
  position: relative;
  line-height: 1.7;
  font-size: 22px;
  padding: 56px;
}

/* Per-slide variants via the _class directive (warm, teal): section:nth-child never matches in Marp Core. */
section.warm {
  background: linear-gradient(135deg, #8e2a6e 0%, #b4232f 100%);
}

section.teal {
  background: linear-gradient(135deg, #1e3a8a 0%, #0f5257 100%);
}

h1, h2, h3, h4, h5, h6 {
  font-weight: 700;
  color: var(--color-heading);
  margin: 0;
  padding: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

h1 {
  font-size: 56px;
  line-height: 1.4;
  text-align: left;
}

h2 {
  position: absolute;
  top: 40px;
  left: 56px;
  right: 56px;
  font-size: 40px;
  padding-top: 0;
  padding-bottom: 16px;
}

h2::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 8px;
  width: 80px;
  height: 3px;
  background-color: var(--color-accent);
  box-shadow: 0 2px 10px rgba(255, 215, 0, 0.5);
}

h2 + * {
  margin-top: 112px;
}

h3 {
  color: var(--color-accent);
  font-size: 28px;
  margin-top: 32px;
  margin-bottom: 12px;
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

ul, ol {
  padding-left: 32px;
}

li {
  margin-bottom: 10px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

section::after {
  color: rgba(255, 255, 255, 0.85);
}

footer {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
  position: absolute;
  left: 56px;
  right: 56px;
  bottom: 40px;
  text-align: center;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

section.lead {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

section.lead h1 {
  margin-bottom: 24px;
  text-align: center;
}

section.lead p {
  font-size: 24px;
  color: var(--color-foreground);
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

strong {
  color: var(--color-accent);
  font-weight: 700;
  text-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
}
</style>

<!-- _class: lead -->

# Presentation

Gradient Background

---

## Agenda

- Topic1
- Topic2
- Topic3

---

<!-- _class: warm -->

## Slide

- Point1
- Point2
- Point3

---

<!-- _class: teal -->

## Slide

- Point1
- Point2
- Point3
