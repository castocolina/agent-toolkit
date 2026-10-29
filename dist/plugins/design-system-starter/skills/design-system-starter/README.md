# Design System Starter

A Claude Code skill for creating and evolving shared design-system contracts, tokens, component guidance, accessibility checks, and adoption documentation.

## Purpose

This skill helps you build robust, scalable design systems that ensure visual consistency and exceptional user experiences across your products. It provides structured guidance for:

- Defining and organizing design tokens (colors, typography, spacing, shadows)
- Deriving reusable component hierarchies from real product use
- Implementing theming and dark mode support
- Ensuring WCAG 2.1 Level AA accessibility compliance
- Creating comprehensive component documentation
- Establishing maintainable design system workflows

## When to Use

Use this skill when you need to:

- Create a new design system from scratch
- Standardize UI patterns across multiple products
- Implement design tokens for consistent styling
- Define reusable component contracts from real product patterns
- Ensure accessibility compliance (WCAG 2.1 AA)
- Set up theming and dark mode support
- Document component libraries effectively
- Migrate from inconsistent UI patterns to a unified system

## How It Works

The skill provides a workflow, a token output template, a component source scaffold, an audit checklist, and component API examples:

### 1. Design Tokens
Structured JSON templates for defining foundational design decisions:
- **Color systems**: Primitive colors (50-950 scale) and semantic tokens (brand, text, background, feedback)
- **Typography**: Font families, sizes, weights, line heights, letter spacing
- **Spacing**: Consistent scale based on 4px or 8px units
- **Border radius**: Reusable corner rounding values
- **Shadows**: Elevation system for depth

### 2. Component Architecture
A reusable component hierarchy based on observed use, with foundational tokens/primitives, composed patterns, and product-level modules only where needed.

### 3. Accessibility
Built-in WCAG 2.1 Level AA compliance:
- Color contrast validation (4.5:1 for normal text, 3:1 for large text)
- Keyboard navigation patterns
- ARIA attributes and screen reader support
- Focus management

### 4. Theming
Defaults to semantic CSS custom properties switched by a `data-theme` attribute, while reusing an existing styling system where appropriate.

### 5. Documentation
Standards for component documentation:
- Component purpose and usage
- Props API with types and defaults
- Accessibility notes
- Common examples

## Key Features

### Design Token System
- W3C design tokens format
- Primitive and semantic color systems
- Typography scales with accessibility in mind
- Consistent spacing based on mathematical scale
- Shadow system for elevation

### Component Guidance
- Semantic component contracts and props
- Composition and slots for genuine variation
- Accessible interaction patterns and validation

### Bundled Resources
The skill includes ready-to-use templates and references:
- `templates/design-tokens-template.json` - Complete token structure
- `templates/component-template.tsx` - Component source scaffold
- `references/component-examples.md` - Field composition, semantic CSS, and token/variant examples
- `checklists/design-system-checklist.md` - Audit checklist

### Accessibility First
- Contrast checks for actual foreground/background pairs
- Color contrast guidelines and testing recommendations
- Keyboard navigation patterns
- ARIA best practices
- Screen reader support patterns

## Usage Examples

### Example 1: Create a New Design System

```
Create a design system for my React app with dark mode support
```

The skill will guide you through:
1. Setting up design tokens (colors, typography, spacing)
2. Deriving reusable component contracts for high-frequency patterns
3. Implementing dark mode with CSS variables
4. Ensuring accessibility compliance
5. Setting up documentation structure

### Example 2: Add Design Tokens

```
Set up design tokens for colors and spacing using the 8px scale
```

Provides:
- Color token structure (primitive + semantic)
- Spacing scale based on 8px units
- W3C design-token JSON structure (see the template's `$schema`)
- CSS variable implementation

### Example 3: Component Architecture

```
Design reusable component contracts for the patterns in my dashboard
```

Delivers:
- A hierarchy based on observed reuse
- Component contracts and composition guidance
- Accessibility and theme considerations

### Example 4: Accessibility Audit

```
Ensure WCAG 2.1 compliance for my button components
```

Checks:
- Color contrast ratios
- Keyboard navigation support
- ARIA attributes
- Focus states
- Screen reader announcements

### Example 5: Theming Implementation

```
Implement theming with dark mode using CSS variables
```

Provides:
- CSS custom property structure
- Light/dark theme definitions
- Theme switching logic
- Component integration patterns

## Triggers

The skill activates on these common phrases:

| Trigger Phrase | What It Does |
|---------------|--------------|
| "Create a design system" | Full design system setup |
| "Set up design tokens" | Token structure and implementation |
| "Design component structure" | Reusable component hierarchy |
| "Ensure WCAG compliance" | Accessibility guidelines and patterns |
| "Implement dark mode" | Theming and dark mode support |
| "Component architecture" | Component organization patterns |
| "Accessibility guidelines" | WCAG 2.1 AA compliance |

## Output Examples

### Design Tokens Output
Complete JSON structure with:
- Color primitives (50-950 scale for each hue)
- Semantic color tokens mapped to primitives
- Typography scale (xs to 5xl)
- Spacing scale (0 to 24)
- Border radius and shadow tokens

### Component Architecture Output
- Component hierarchy and inventory based on observed patterns
- Props interface definitions
- Implementation examples with TypeScript
- Accessibility notes for each component

### Theming Output
- Theme structure interface
- Light and dark theme definitions
- CSS variable mapping
- Theme provider setup
- Component integration patterns

### Accessibility Checklist Output
- Color contrast validation results
- Keyboard navigation requirements
- ARIA attribute recommendations
- Screen reader testing notes
- Focus management patterns

## Design Philosophy

The skill is built on four core principles:

1. **Consistency Over Creativity**: Predictable patterns reduce cognitive load and help users learn once, apply everywhere

2. **Accessible by Default**: WCAG 2.1 Level AA compliance minimum, keyboard navigation built-in, screen reader support from the start

3. **Scalable and Maintainable**: Design tokens enable global changes, component composition reduces duplication

4. **Developer-Friendly**: Clear API contracts, comprehensive documentation, easy to integrate and customize

## License

MIT

## Version

1.0.0
