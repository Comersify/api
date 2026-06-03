# Responsive Design Guide

Strategies for building responsive Django admin interfaces that work across all devices.

## Breakpoint Strategy

### Standard Breakpoints

```css
/* Mobile first approach */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }

/* Or use max-width for mobile-first */
@media (max-width: 639px) { }
@media (max-width: 767px) { }
@media (max-width: 1023px) { }
@media (max-width: 1279px) { }
```

### Admin-Specific Breakpoints

```css
/* Desktop: Full sidebar */
@media (min-width: 1024px) {
  #nav-sidebar {
    transform: translateX(0);
  }
  #main {
    margin-left: 280px;
  }
}

/* Tablet: Collapsible sidebar */
@media (max-width: 1023px) {
  #nav-sidebar {
    transform: translateX(-100%);
  }
  #nav-sidebar.open {
    transform: translateX(0);
  }
  #main {
    margin-left: 0;
  }
}

/* Mobile: Drawer navigation */
@media (max-width: 767px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  .module-card {
    margin-bottom: 1rem;
  }
}
```

## Sidebar Responsiveness

### Collapsible Sidebar

```css
#nav-sidebar {
  width: 280px;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 50;
  transition: transform 0.2s;
}

@media (max-width: 1023px) {
  #nav-sidebar {
    transform: translateX(-100%);
  }
  
  #nav-sidebar.open {
    transform: translateX(0);
  }
}

/* Mobile menu toggle button */
.mobile-menu-btn {
  display: none;
  padding: 0.5rem;
  background: transparent;
  border: none;
  cursor: pointer;
}

@media (max-width: 1023px) {
  .mobile-menu-btn {
    display: flex;
  }
}
```

### Overlay for Mobile

```css
#nav-sidebar::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
}

#nav-sidebar.open::before {
  opacity: 1;
  pointer-events: auto;
}
```

## Grid Layouts

### Dashboard Grid

```css
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
```

### Stats Grid

```css
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
```

### Module Cards Grid

```css
.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

@media (max-width: 1024px) {
  .modules-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
}

@media (max-width: 640px) {
  .modules-grid {
    grid-template-columns: 1fr;
  }
}
```

## Table Responsiveness

### Horizontal Scroll

```css
.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

table {
  min-width: 600px;
}
```

### Card View on Mobile

Instead of tables on mobile, consider card-based layouts:

```css
@media (max-width: 767px) {
  /* Hide table, show cards instead */
  .results-table {
    display: none;
  }
  
  .mobile-cards {
    display: block;
  }
  
  .mobile-card {
    background: hsl(var(--card));
    border: 1px solid hsl(var(--border));
    border-radius: var(--radius);
    padding: 1rem;
    margin-bottom: 0.75rem;
  }
}
```

### Responsive Columns

```css
/* Hide less important columns on mobile */
@media (max-width: 767px) {
  .hide-mobile {
    display: none;
  }
}

/* Show additional columns on desktop */
@media (min-width: 1024px) {
  .hide-desktop {
    display: none;
  }
  .show-desktop {
    display: table-cell;
  }
}
```

## Form Responsiveness

### Full Width on Mobile

```css
.form-input,
.form-select {
  width: 100%;
}

/* Stack form fields */
@media (max-width: 640px) {
  .form-row {
    flex-direction: column;
  }
  
  .form-row > * {
    width: 100%;
    margin-bottom: 0.5rem;
  }
}
```

### Two Column Forms

```css
@media (min-width: 768px) {
  .two-column-form {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}
```

## Header Responsiveness

```css
#header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
  height: 64px;
}

@media (max-width: 640px) {
  #header {
    padding: 0 0.75rem;
  }
  
  #branding span:not(.site-icon) {
    display: none;
  }
}
```

## Pagination Responsiveness

```css
.pagination-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 640px) {
  .pagination-container {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}
```

## Action Bar Responsiveness

```css
.actions-bar {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

@media (min-width: 640px) {
  .actions-bar {
    flex-direction: row;
    align-items: center;
  }
  
  .actions-count {
    margin-left: auto;
  }
}
```

## Content Padding

```css
.content {
  padding: 1.5rem;
  max-width: 1400px;
}

@media (max-width: 640px) {
  .content {
    padding: 1rem;
  }
}
```

## Page Header Responsiveness

```css
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  gap: 1rem;
}

@media (max-width: 640px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
```

## Quick Actions Responsiveness

```css
.quick-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

@media (max-width: 640px) {
  .quick-actions {
    flex-direction: column;
  }
  
  .quick-action {
    width: 100%;
    justify-content: center;
  }
}
```

## Touch-Friendly Targets

```css
/* Minimum touch target size */
@media (max-width: 767px) {
  a, button {
    min-height: 44px;
    min-width: 44px;
  }
}

/* Larger touch targets for actions */
.action-btn,
.pagination-link {
  padding: 0.75rem 1rem;
}
```

## Loading States for Mobile

```css
@media (max-width: 640px) {
  /* Skeleton loading */
  .skeleton {
    background: linear-gradient(
      90deg,
      hsl(var(--muted)) 25%,
      hsl(var(--muted-foreground) / 0.1) 50%,
      hsl(var(--muted)) 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
  }
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

## Print Styles

```css
@media print {
  #nav-sidebar,
  #header,
  .actions-bar,
  .pagination {
    display: none !important;
  }
  
  #main {
    margin: 0;
  }
  
  .content {
    max-width: 100%;
    padding: 0;
  }
  
  table {
    page-break-inside: avoid;
  }
}
```

## Testing Checklist

- [ ] Mobile (320px): Full layout works
- [ ] Tablet (768px): Grid adapts
- [ ] Desktop (1024px): Full sidebar visible
- [ ] Large (1280px+): Comfortable spacing
- [ ] Touch devices: Large tap targets
- [ ] Keyboard navigation: All elements accessible
- [ ] Print: Clean output

## Common Issues

### Sidebar blocking content on mobile

Solution: Ensure main content has margin-left when sidebar visible, or overlay mode.

### Tables overflow container

Solution: Wrap tables in `.table-container { overflow-x: auto; }`

### Forms too narrow on mobile

Solution: Use full width inputs, stack fields vertically.

### Buttons too small on touch devices

Solution: Increase padding, ensure minimum 44px tap target.

### Text too small on high DPI screens

Solution: Use relative units (rem, em) not pixels for font sizes.