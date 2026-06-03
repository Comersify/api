# Component Patterns

Reusable CSS patterns for shadcn-inspired Django admin components.

## Card Components

### Basic Card

```css
.card {
  background: hsl(var(--card));
  border-radius: calc(var(--radius) + 4px);
  border: 1px solid hsl(var(--border));
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid hsl(var(--border));
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: hsl(var(--foreground));
}

.card-content {
  padding: 1.5rem;
}

.card-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid hsl(var(--border));
  display: flex;
  gap: 0.75rem;
}
```

### Stat Card

```css
.stat-card {
  background: hsl(var(--card));
  border-radius: calc(var(--radius) + 4px);
  border: 1px solid hsl(var(--border));
  padding: 1.25rem;
  position: relative;
  overflow: hidden;
}

.stat-card:hover {
  box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.1);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, hsl(var(--primary)) 0%, transparent 100%);
  opacity: 0;
  transition: opacity 0.2s;
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.stat-icon.primary {
  background: hsl(var(--primary) / 0.1);
  color: hsl(var(--primary));
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: hsl(var(--foreground));
  letter-spacing: -0.025em;
}

.stat-label {
  font-size: 0.8125rem;
  color: hsl(var(--muted-foreground));
}
```

### Module Card (Dashboard)

```css
.module-card {
  background: hsl(var(--card));
  border-radius: calc(var(--radius) + 4px);
  border: 1px solid hsl(var(--border));
  padding: 1.25rem;
  transition: all 0.2s;
}

.module-card:hover {
  box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.1);
  border-color: hsl(var(--primary) / 0.3);
}

.module-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid hsl(var(--border));
}

.module-icon {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: hsl(var(--primary) / 0.1);
  color: hsl(var(--primary));
}

.module-title {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

## Button Components

### Base Button

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.15s;
}

.btn:hover {
  transform: translateY(-1px);
}
```

### Primary Button

```css
.btn-primary {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
}

.btn-primary:hover {
  background: hsl(221.2 83.2% 45%);
  box-shadow: 0 4px 12px -2px rgba(59, 130, 246, 0.4);
}
```

### Secondary Button

```css
.btn-secondary {
  background: hsl(var(--secondary));
  color: hsl(var(--secondary-foreground));
  border-color: hsl(var(--border));
}

.btn-secondary:hover {
  background: hsl(var(--accent));
}
```

### Destructive Button

```css
.btn-destructive {
  background: hsl(var(--destructive));
  color: hsl(var(--destructive-foreground));
}

.btn-destructive:hover {
  background: hsl(0 84.2% 50%);
}
```

### Outline Button

```css
.btn-outline {
  border-color: hsl(var(--border));
  background: transparent;
}

.btn-outline:hover {
  background: hsl(var(--accent));
}
```

### Ghost Button

```css
.btn-ghost {
  background: transparent;
}

.btn-ghost:hover {
  background: hsl(var(--accent));
}
```

### Button Sizes

```css
.btn-sm {
  padding: 0.375rem 0.625rem;
  font-size: 0.8125rem;
}

.btn-lg {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

.btn-icon {
  padding: 0.5rem;
  width: 2.5rem;
  height: 2.5rem;
}
```

## Form Components

### Form Group

```css
.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.375rem;
  color: hsl(var(--foreground));
}

.form-label.required::after {
  content: " *";
  color: hsl(var(--destructive));
}
```

### Input Field

```css
.form-input {
  display: flex;
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid hsl(var(--input));
  border-radius: var(--radius);
  font-size: 0.875rem;
  background: hsl(var(--background));
  color: hsl(var(--foreground));
  transition: all 0.15s;
}

.form-input:focus {
  outline: none;
  border-color: hsl(var(--ring));
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  transform: scale(1.01);
}

.form-input::placeholder {
  color: hsl(var(--muted-foreground));
}
```

### Select Field

```css
.form-select {
  display: flex;
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid hsl(var(--input));
  border-radius: var(--radius);
  font-size: 0.875rem;
  background: hsl(var(--background));
  cursor: pointer;
}

.form-select:focus {
  outline: none;
  border-color: hsl(var(--ring));
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}
```

### Checkbox

```css
.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox {
  width: 1rem;
  height: 1rem;
  border: 1px solid hsl(var(--input));
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.checkbox:checked {
  background: hsl(var(--primary));
  border-color: hsl(var(--primary));
}

.checkbox-label {
  font-size: 0.875rem;
  color: hsl(var(--foreground));
}
```

### Form Help & Error

```css
.form-help {
  font-size: 0.8125rem;
  color: hsl(var(--muted-foreground));
  margin-top: 0.25rem;
}

.form-error {
  font-size: 0.8125rem;
  color: hsl(var(--destructive));
  margin-top: 0.25rem;
}
```

## Table Components

### Basic Table

```css
.table-container {
  border: 1px solid hsl(var(--border));
  border-radius: calc(var(--radius) + 4px);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: hsl(var(--muted));
}

th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: hsl(var(--muted-foreground));
  border-bottom: 1px solid hsl(var(--border));
}

td {
  padding: 0.875rem 1rem;
  border-bottom: 1px solid hsl(var(--border));
}

tbody tr:hover {
  background: hsl(var(--accent));
}

tbody tr:last-child td {
  border-bottom: none;
}
```

### Results Table (Admin)

```css
.results-container {
  background: hsl(var(--card));
  border-radius: calc(var(--radius) + 4px);
  border: 1px solid hsl(var(--border));
  overflow: hidden;
}

.results-table th.sortable a {
  color: hsl(var(--muted-foreground));
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.row-actions {
  display: flex;
  gap: 0.25rem;
}

.row-actions a,
.row-actions button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.375rem;
  border-radius: 4px;
  color: hsl(var(--muted-foreground));
}

.row-actions a:hover {
  background: hsl(var(--accent));
  color: hsl(var(--foreground));
}

.row-actions .delete:hover {
  background: hsl(var(--destructive) / 0.1);
  color: hsl(var(--destructive));
}
```

## Badge/Pill Components

### Basic Badge

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

### Badge Variants

```css
.badge-default {
  background: hsl(var(--secondary));
  color: hsl(var(--secondary-foreground));
}

.badge-primary {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
}

.badge-secondary {
  background: hsl(var(--accent));
  color: hsl(var(--accent-foreground));
}

.badge-destructive {
  background: hsl(var(--destructive));
  color: hsl(var(--destructive-foreground));
}

.badge-success {
  background: hsl(142.1 76.2% 36.3%);
  color: white;
}

.badge-warning {
  background: hsl(48 96% 53%);
  color: hsl(25 95% 53%);
}

.badge-outline {
  border: 1px solid hsl(var(--border));
  background: transparent;
  color: hsl(var(--foreground));
}
```

## Navigation Components

### Breadcrumbs

```css
.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 0;
  font-size: 0.875rem;
}

.breadcrumbs a {
  color: hsl(var(--muted-foreground));
  text-decoration: none;
}

.breadcrumbs a:hover {
  color: hsl(var(--primary));
}

.breadcrumbs-separator {
  color: hsl(var(--muted-foreground));
}

.breadcrumbs-current {
  color: hsl(var(--foreground));
  font-weight: 500;
}
```

### Tabs

```css
.tabs {
  display: flex;
  gap: 0.25rem;
  border-bottom: 1px solid hsl(var(--border));
  margin-bottom: 1rem;
}

.tab {
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: hsl(var(--muted-foreground));
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: all 0.15s;
}

.tab:hover {
  color: hsl(var(--foreground));
}

.tab.active {
  color: hsl(var(--primary));
  border-bottom-color: hsl(var(--primary));
}
```

### Sidebar Navigation

```css
.module-list {
  padding: 1rem 0;
  overflow-y: auto;
}

.app-group {
  margin-bottom: 0.5rem;
}

.app-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: hsl(var(--muted-foreground));
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.app-models a {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.625rem 0.875rem;
  border-radius: var(--radius);
  font-size: 0.875rem;
  color: hsl(var(--foreground));
  text-decoration: none;
  transition: all 0.15s;
}

.app-models a:hover {
  background: hsl(var(--accent));
}

.app-models a.active {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
}
```

## Pagination Components

```css
.pagination-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
  border-top: 1px solid hsl(var(--border));
}

.pagination-info {
  font-size: 0.875rem;
  color: hsl(var(--muted-foreground));
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.pagination-link {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 2rem;
  height: 2rem;
  padding: 0 0.5rem;
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
  font-size: 0.875rem;
  color: hsl(var(--foreground));
  text-decoration: none;
}

.pagination-link:hover {
  background: hsl(var(--accent));
}

.pagination-link.active {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
  border-color: hsl(var(--primary));
}
```

## Alert Components

```css
.alert {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: var(--radius);
  margin-bottom: 1rem;
}

.alert-info {
  background: hsl(221.2 83.2% 53.3% / 0.1);
  border: 1px solid hsl(221.2 83.2% 53.3% / 0.2);
}

.alert-success {
  background: hsl(142.1 76.2% 36.3% / 0.1);
  border: 1px solid hsl(142.1 76.2% 36.3% / 0.2);
}

.alert-warning {
  background: hsl(48 96% 53% / 0.1);
  border: 1px solid hsl(48 96% 53% / 0.2);
}

.alert-error {
  background: hsl(var(--destructive) / 0.1);
  border: 1px solid hsl(var(--destructive) / 0.2);
}
```

## Empty State Component

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1.5rem;
  text-align: center;
}

.empty-state-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: hsl(var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.empty-state-title {
  font-size: 1rem;
  font-weight: 600;
  color: hsl(var(--foreground));
  margin-bottom: 0.375rem;
}

.empty-state-description {
  font-size: 0.875rem;
  color: hsl(var(--muted-foreground));
  margin-bottom: 1.5rem;
}
```

## Action Bar Component

```css
.actions-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: hsl(var(--muted));
  border-radius: var(--radius);
  margin-bottom: 1rem;
}

.actions-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid hsl(var(--input));
  border-radius: var(--radius);
  font-size: 0.875rem;
  background: hsl(var(--background));
}

.actions-btn {
  padding: 0.5rem 0.75rem;
  background: hsl(var(--secondary));
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
  font-size: 0.875rem;
}

.actions-btn:hover {
  background: hsl(var(--accent));
}

.actions-count {
  margin-left: auto;
  font-size: 0.875rem;
  color: hsl(var(--muted-foreground));
}
```

## Fieldset Component

```css
.fieldset {
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
  padding: 1.25rem;
  margin-bottom: 1.25rem;
}

.fieldset-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: hsl(var(--foreground));
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid hsl(var(--border));
}
```

## Login Card Pattern

```css
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, hsl(var(--background)) 0%, hsl(var(--muted)) 100%);
  padding: 1.5rem;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: hsl(var(--card));
  border-radius: calc(var(--radius) + 8px);
  border: 1px solid hsl(var(--border));
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
  animation: slideUp 0.4s ease-out;
}

.login-header {
  padding: 2rem 2rem 0;
  text-align: center;
}

.login-logo-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, hsl(var(--primary)) 0%, hsl(221.2 83.2% 40%) 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  margin: 0 auto 1rem;
  box-shadow: 0 8px 24px -4px rgba(59, 130, 246, 0.4);
}

.login-form {
  padding: 1.5rem 2rem 2rem;
}

.login-submit {
  width: 100%;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, hsl(var(--primary)) 0%, hsl(221.2 83.2% 45%) 100%);
  color: hsl(var(--primary-foreground));
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.4);
}

.login-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px -4px rgba(59, 130, 246, 0.5);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```