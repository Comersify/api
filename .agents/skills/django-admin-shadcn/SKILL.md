---
name: django-admin-shadcn
description: This skill should be used when the user asks to "upgrade Django admin to shadcn", "transform admin to modern dashboard", "apply shadcn ui to Django", "create shadcn style admin", "migrate admin to Tailwind CSS", "build modern Django admin", "style admin with shadcn components", "upgrade admin dashboard design". Provides comprehensive guidance for transforming Django admin dashboards into modern, production-quality shadcn/ui-inspired interfaces using Tailwind CSS while preserving all backend functionality.
---

# Django Admin Shadcn Transformation

Transform any Django admin dashboard into a modern, shadcn/ui-inspired interface using Tailwind CSS. Preserve all backend functionality while achieving a premium SaaS dashboard appearance.

## Core Principles

1. **Preserve Functionality**: Never modify Python code, URL routing, authentication, or business logic
2. **Visual First**: Focus on CSS/Tailwind transformations, not backend changes
3. **Responsive Design**: Ensure mobile-friendly layouts with proper breakpoints
4. **Accessibility**: Maintain WCAG compliance with visible focus states and semantic HTML
5. **Progressive Enhancement**: Build upon Django's default templates, not replace them

## Workflow

### Step 1: Analyze Existing Templates

Start by examining current admin templates:
```
django-admin-shadcn/assets/base_template.html  # Reference for structure
```

Review the installed templates:
```bash
ls -la templates/admin/
cat templates/admin/base.html
```

### Step 2: Create CSS Foundation

Create custom CSS file with Tailwind-inspired design tokens:
```
static/admin/css/shadcn-admin.css
```

Include in templates via `{% block extrastyle %}`:
```django
{% block extrastyle %}
{{ block.super }}
<link rel="stylesheet" href="{% static 'admin/css/shadcn-admin.css' %}">
{% endblock %}
```

### Step 3: Define Design System

Create CSS variables following shadcn design tokens:

```css
:root {
  /* Base Colors */
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;
  --secondary: 210 40% 96.1%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --border: 214.3 31.8% 91.4%;
  --radius: 0.5rem;
}
```

### Step 4: Component Upgrades

Apply consistent styling to:

- **Header**: Sticky navbar with branding, user menu
- **Sidebar**: Collapsible navigation with icons
- **Cards**: Rounded corners, subtle shadows, hover states
- **Tables**: Striped rows, hover highlights, sticky headers
- **Forms**: Modern inputs with focus rings, inline validation
- **Buttons**: Gradient primary, outlined secondary, destructive red

### Step 5: Template Overrides

Create minimal template overrides that extend Django defaults:

```django
{% extends "admin/base.html" %}
{% load static i18n %}

{% block extrastyle %}
{{ block.super }}
<link rel="stylesheet" href="{% static 'admin/css/shadcn-admin.css' %}">
{% endblock %}
```

### Step 6: Test Responsiveness

Verify across breakpoints:
- Desktop (1024px+): Full sidebar visible
- Tablet (768px-1023px): Collapsible sidebar
- Mobile (<768px): Drawer navigation

## Key Components

### Design Tokens

Reference the complete design system in:
- **`references/design-tokens.md`** - Full color palette, typography, spacing

### CSS Structure

Organize CSS by component:

```css
/* ==========================================================================
   Layout
   ========================================================================== */
/* Header, Sidebar, Main Content */

/* ==========================================================================
   Components
   ========================================================================== */
/* Cards, Tables, Forms, Buttons */

/* ==========================================================================
   Utilities
   ========================================================================== */
/* Spacing, Typography, Colors */
```

### Common Patterns

**Card Component:**
```css
.card {
  background: hsl(var(--card));
  border-radius: calc(var(--radius) + 4px);
  border: 1px solid hsl(var(--border));
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}
```

**Button Variants:**
```css
.btn-primary {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
}
.btn-secondary {
  background: hsl(var(--secondary));
  border: 1px solid hsl(var(--border));
}
```

**Table Styling:**
```css
table {
  border-collapse: collapse;
}
th {
  background: hsl(var(--muted));
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
tr:hover td {
  background: hsl(var(--accent));
}
```

## File Structure

```
django-admin-shadcn/
├── SKILL.md
├── references/
│   ├── design-tokens.md      # Complete color palette, typography
│   ├── component-patterns.md # Reusable component styles
│   └── responsive-guide.md    # Breakpoint strategies
├── scripts/
│   └── validate_css.sh       # CSS validation utility
└── assets/
    └── base_template.html    # Reference template structure
```

## Reference Files

### **`references/design-tokens.md`**
Complete shadcn design system:
- Color palette (background, foreground, primary, secondary, muted, destructive)
- Typography scale (font families, sizes, weights)
- Spacing system (padding, margins)
- Border radius values
- Shadow presets

### **`references/component-patterns.md`**
Reusable component patterns:
- Card layouts
- Table structures
- Form inputs
- Button groups
- Navigation menus
- Empty states
- Loading skeletons

### **`references/responsive-guide.md`**
Responsive design strategies:
- Mobile-first approach
- Breakpoint definitions
- Sidebar collapse behavior
- Table scroll modes
- Form stacking

## Authentication Handling

For email-based authentication in Django admin:

1. Create custom auth backend in `user/backends.py`:
```python
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
```

2. Add to settings:
```python
AUTHENTICATION_BACKENDS = [
    'user.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

## Django Admin Specifics

### Template Loading Order

Django looks for admin templates in this order:
1. `templates/admin/` (custom overrides)
2. App-specific templates
3. Django's default templates

### Key Template Blocks

- `{% block extrastyle %}` - Add custom CSS
- `{% block branding %}` - Customize header
- `{% block nav-global %}` - Add global navigation
- `{% block content %}` - Main content area

### Preserving Django Features

Always preserve:
- `{% csrf_token %}` in forms
- `{{ form.as_p }}` or `{{ form.as_table }}` for form rendering
- Django's built-in validation
- Admin's permission system

## Quality Checklist

- [ ] All templates extend Django defaults
- [ ] CSS variables define complete design system
- [ ] Light and dark mode support
- [ ] Mobile-responsive sidebar
- [ ] Form inputs have visible focus states
- [ ] Tables have hover highlighting
- [ ] Buttons have consistent styling
- [ ] No inline styles (use CSS classes)
- [ ] Semantic HTML maintained
- [ ] Django functionality preserved

## Common Transformations

### Login Page
- Centered card with animated background
- Pulsing logo icon
- Error shake animation
- Modern form inputs

### Dashboard Index
- Stats cards with trend indicators
- Grid layout for app modules
- Activity feed styling
- Quick action buttons

### Change List (List View)
- Clean table with borders
- Filter sidebar
- Search with icon
- Pagination controls

### Change Form (Edit/Create)
- Two-column layout for fieldsets
- Modern form inputs
- Save/Cancel buttons with icons
- Delete with confirmation

## Performance Considerations

- Minify CSS in production
- Use CSS variables for theming
- Lazy load non-critical styles
- Preconnect to Google Fonts
- Optimize images in admin

## Troubleshooting

**Template not loading?**
- Check `TEMPLATES` setting in `settings.py`
- Verify `APP_DIRS: true` in TEMPLATES config

**CSS not applying?**
- Run `python manage.py collectstatic`
- Clear browser cache
- Check for caching middleware

**Django errors after changes?**
- Verify template syntax with `{% load i18n %}`
- Check for missing translation tags
- Run `python manage.py check`

## Summary

Transform Django admin to shadcn/ui by:
1. Creating custom CSS with design tokens
2. Minimal template overrides extending defaults
3. Preserving all Django functionality
4. Applying consistent component styling
5. Ensuring responsive behavior

The goal is a modern dashboard that looks like shadcn/ui while fully leveraging Django's admin system.