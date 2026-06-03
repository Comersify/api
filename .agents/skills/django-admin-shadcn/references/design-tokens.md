# Design Tokens - Complete Reference

## Color Palette

### HSL Color Variables

Use HSL values with CSS variables for consistent theming:

```css
:root {
  /* Background & Foreground */
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  
  /* Card */
  --card: 0 0% 100%;
  --card-foreground: 222.2 84% 4.9%;
  
  /* Popover */
  --popover: 0 0% 100%;
  --popover-foreground: 222.2 84% 4.9%;
  
  /* Primary */
  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;
  
  /* Secondary */
  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;
  
  /* Muted */
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  
  /* Accent */
  --accent: 210 40% 96.1%;
  --accent-foreground: 222.2 47.4% 11.2%;
  
  /* Destructive */
  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 210 40% 98%;
  
  /* Border & Input */
  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;
  --ring: 221.2 83.2% 53.3%;
  
  /* Radius */
  --radius: 0.5rem;
}
```

### Dark Mode Colors

```css
.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --card: 222.2 84% 4.9%;
  --card-foreground: 210 40% 98%;
  --primary: 217.2 91.2% 59.8%;
  --primary-foreground: 222.2 47.4% 11.2%;
  --secondary: 217.2 32.6% 17.5%;
  --secondary-foreground: 210 40% 98%;
  --muted: 217.2 32.6% 17.5%;
  --muted-foreground: 215 20.2% 65.1%;
  --accent: 217.2 32.6% 17.5%;
  --accent-foreground: 210 40% 98%;
  --destructive: 0 62.8% 30.6%;
  --destructive-foreground: 210 40% 98%;
  --border: 217.2 32.6% 17.5%;
  --input: 217.2 32.6% 17.5%;
  --ring: 224.3 76.3% 48%;
}
```

### Semantic Colors

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `background` | White | Near black | Page background |
| `foreground` | Dark slate | Off white | Primary text |
| `primary` | Blue | Lighter blue | Primary actions |
| `secondary` | Light gray | Dark gray | Secondary actions |
| `muted` | Very light gray | Darker gray | Subtle backgrounds |
| `destructive` | Red | Darker red | Delete, errors |
| `border` | Gray | Dark gray | Borders |
| `accent` | Light gray | Medium gray | Hover states |

## Typography

### Font Stack

```css
font-family: 'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Type Scale

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 | 1.875rem (30px) | 700 | 1.2 |
| H2 | 1.5rem (24px) | 700 | 1.3 |
| H3 | 1.25rem (20px) | 600 | 1.4 |
| H4 | 1rem (16px) | 600 | 1.5 |
| Body | 0.875rem (14px) | 400 | 1.6 |
| Small | 0.75rem (12px) | 400 | 1.5 |
| Tiny | 0.6875rem (11px) | 500 | 1.4 |

### Font Weights

| Weight | Value | Usage |
|--------|-------|-------|
| Normal | 400 | Body text |
| Medium | 500 | Emphasis, labels |
| Semibold | 600 | Headings, buttons |
| Bold | 700 | Page titles |

### Letter Spacing

| Element | Value |
|---------|-------|
| Headings | -0.025em |
| Body | 0 |
| Uppercase labels | 0.05em |

## Spacing System

### Base Unit: 4px

```css
--spacing-1: 0.25rem;  /* 4px */
--spacing-2: 0.5rem;   /* 8px */
--spacing-3: 0.75rem;   /* 12px */
--spacing-4: 1rem;      /* 16px */
--spacing-5: 1.25rem;   /* 20px */
--spacing-6: 1.5rem;    /* 24px */
--spacing-8: 2rem;      /* 32px */
--spacing-10: 2.5rem;   /* 40px */
--spacing-12: 3rem;     /* 48px */
```

### Padding Patterns

```css
/* Card padding */
padding: 1.25rem; /* 20px */

/* Form field spacing */
margin-bottom: 1.25rem; /* 20px */

/* Table cell */
padding: 0.875rem 1rem; /* 14px 16px */

/* Button padding */
padding: 0.5rem 1rem; /* 8px 16px */
```

## Border Radius

```css
/* Small (inputs, buttons) */
--radius: 0.5rem; /* 8px */

/* Medium (cards) */
--radius-md: calc(var(--radius) + 4px); /* 12px */

/* Large (modals) */
--radius-lg: calc(var(--radius) + 8px); /* 16px */

/* Full (pills) */
--radius-full: 9999px;
```

### Specific Border Radius

| Element | Radius |
|---------|--------|
| Buttons | 6px (var(--radius)) |
| Inputs | 6px |
| Cards | 12px |
| Modals | 16px |
| Badges | 9999px (pill) |

## Shadows

### Elevation Levels

```css
/* Subtle (cards default) */
box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);

/* Medium (cards hover) */
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);

/* Large (modals, dropdowns) */
box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);

/* Extra large (login cards) */
box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
```

### Primary Button Shadow

```css
box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.4);
```

## Breakpoints

### Standard Breakpoints

```css
/* Mobile */
@media (max-width: 640px) { }

/* Tablet */
@media (max-width: 768px) { }

/* Desktop */
@media (max-width: 1024px) { }

/* Large Desktop */
@media (max-width: 1280px) { }
```

### Grid Columns

```css
/* Mobile: 1 column */
grid-template-columns: 1fr;

/* Tablet: 2 columns */
grid-template-columns: repeat(2, 1fr);

/* Desktop: 3-4 columns */
grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
```

## Z-Index Scale

| Layer | Value | Usage |
|-------|-------|-------|
| Base | 0 | Default elements |
| Dropdown | 40 | Menus, dropdowns |
| Sticky | 50 | Fixed headers |
| Modal | 100 | Dialogs |
| Popover | 200 | Tooltips |
| Toast | 300 | Notifications |

## Transitions

### Timing Functions

```css
transition: all 0.15s ease; /* Default */
transition: all 0.2s ease; /* Hover states */
transition: all 0.3s ease-out; /* Entrance animations */
```

### Common Transitions

| Element | Duration | Property |
|---------|----------|----------|
| Buttons | 0.15s | all |
| Cards | 0.2s | all |
| Modals | 0.3s | transform, opacity |
| Sidebar | 0.2s | transform |

## Animations

### Keyframes

```css
/* Fade in */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide up */
@keyframes slideUp {
  from { transform: translateY(10px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* Pulse */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Float (background decoration) */
@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  25% { transform: translate(2%, 2%); }
  50% { transform: translate(0, 4%); }
  75% { transform: translate(-2%, 2%); }
}

/* Shake (error) */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}
```

### Animation Classes

```css
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.4s ease-out;
}
```

## Focus States

### Focus Ring

```css
:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

/* Primary color ring */
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px white, 0 0 0 4px hsl(var(--ring));
}
```

### Input Focus

```css
input:focus {
  border-color: hsl(var(--ring));
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  transform: scale(1.01);
}
```

## Icon Sizes

| Context | Size |
|---------|------|
| Small (inline) | 16px |
| Default | 20px |
| Large (feature) | 24px |
| XL (decorative) | 32px |
| Hero | 48px+ |

## Sidebar Width

```css
--sidebar-width: 280px;
```

## Header Height

```css
--header-height: 64px;
```

## Table Styling

```css
/* Header */
th {
  background: hsl(var(--muted));
  padding: 0.75rem 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: hsl(var(--muted-foreground));
}

/* Cells */
td {
  padding: 0.875rem 1rem;
  border-bottom: 1px solid hsl(var(--border));
  font-size: 0.875rem;
}

/* Hover */
tbody tr:hover td {
  background: hsl(var(--accent));
}
```

## Form Input Styling

```css
input, select, textarea {
  padding: 0.5rem 0.75rem;
  border: 1px solid hsl(var(--input));
  border-radius: var(--radius);
  font-size: 0.875rem;
  background: hsl(var(--background));
}

input:focus, select:focus, textarea:focus {
  border-color: hsl(var(--ring));
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}
```

## Badge/Pill Styling

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}
```