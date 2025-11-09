# Design Document

## Overview

This design document outlines the technical approach for implementing the Google Stitch reference design into the BlogBreeze Django application. The implementation will replace the current Bootstrap 5 styling with Tailwind CSS and restructure templates to match the modern, minimalist aesthetic of the Stitch design.

The design focuses on creating a cohesive visual experience across all pages while maintaining the existing Django architecture and functionality. The key changes include integrating Tailwind CSS, adding a description field to the Post model, and redesigning all templates to match the reference design.

## Architecture

### Technology Stack

- **Frontend Framework**: Tailwind CSS 3.x (via CDN)
- **Font**: Inter (Google Fonts)
- **Icons**: Material Symbols Outlined (Google Fonts)
- **Backend**: Django (existing)
- **Template Engine**: Django Templates (existing)

### Design System

**Color Palette:**
```
Primary: #137fec (blue)
Background Light: #f6f7f8
Background Dark: #101922
Text Light: #101922 / #212121
Text Dark: #f6f7f8 / #f9f9f9
Text Secondary Light: #4c739a / #616161
Text Secondary Dark: #a7b5c4 / #a1a1a1
Card Light: #ffffff
Card Dark: #192734
Border Light: #e7edf3 / #EAEAEA
Border Dark: #2c3a4a / #2D3748
```

**Typography:**
- Display Font: Inter (weights: 400, 500, 600, 700, 900)
- Body Font: Inter for UI, Merriweather for article content
- Base Size: 16px
- Scale: Tailwind's default scale (text-sm, text-base, text-lg, text-xl, etc.)

**Spacing:**
- Uses Tailwind's default spacing scale (4px base unit)
- Container max-width: 1200px (homepage), 960px (content pages)
- Grid gaps: 24px (gap-6) to 32px (gap-8)

**Border Radius:**
- Default: 0.25rem (rounded)
- Large: 0.5rem (rounded-lg)
- Extra Large: 0.75rem (rounded-xl)
- Full: 9999px (rounded-full)

## Components and Interfaces

### 1. Base Template (`templates/base.html`)

**Purpose**: Provides the foundational HTML structure and Tailwind CSS configuration for all pages.

**Structure:**
```html
<!DOCTYPE html>
<html class="light" lang="en">
<head>
    - Meta tags (charset, viewport)
    - Title block
    - Tailwind CSS CDN with plugins (forms, container-queries)
    - Google Fonts (Inter, Material Symbols)
    - Tailwind config script with custom colors
    - Extra CSS block
</head>
<body class="font-display bg-background-light dark:bg-background-dark">
    - Navigation bar (include)
    - Django messages
    - Content block
    - Footer (include)
    - Extra JS block
</body>
</html>
```

**Tailwind Configuration:**
```javascript
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "primary": "#137fec",
        "background-light": "#f6f7f8",
        "background-dark": "#101922",
        // ... other colors
      },
      fontFamily: {
        "display": ["Inter", "sans-serif"]
      },
      borderRadius: {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      }
    }
  }
}
```

### 2. Navigation Bar (`templates/includes/navbar.html`)

**Purpose**: Provides consistent navigation across all pages.

**Structure:**
- Container with max-width and horizontal padding
- Left section: Logo icon + "Modern Blog" text
- Right section: Navigation links (Home, Categories) + Search button
- Responsive: Hide nav links on mobile (hidden sm:flex)
- Border bottom with light/dark mode support

**Styling:**
- Height: py-4 (16px padding)
- Logo: size-6 (24x24px) with primary color
- Links: text-sm font-medium with hover:text-primary
- Search button: rounded-full h-10 w-10 with icon

### 3. Homepage (`templates/blog/post_list.html`)

**Purpose**: Displays the latest post in a hero section and remaining posts in a grid.

**Structure:**

**Hero Section:**
```html
<div class="my-8">
    <div class="flex min-h-[480px] flex-col gap-6 bg-cover bg-center 
                rounded-xl items-start justify-end px-6 pb-10 sm:px-10"
         style="background-image: linear-gradient(...), url(...)">
        <div class="flex flex-col gap-4 text-left max-w-2xl">
            <h1 class="text-white text-4xl font-black sm:text-5xl">
                {{ first_post.title }}
            </h1>
            <h2 class="text-slate-200 text-base sm:text-lg">
                {{ first_post.description|default:first_post.content|truncatewords:30 }}
            </h2>
        </div>
        <button class="... bg-primary text-white ...">
            Read More
        </button>
    </div>
</div>
```

**Post Grid:**
```html
<main class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8 p-4">
    {% for post in remaining_posts %}
    <div class="flex flex-col gap-4 pb-3 rounded-xl overflow-hidden 
                bg-card-light dark:bg-card-dark shadow-sm 
                hover:shadow-lg transition-shadow duration-300">
        <div class="w-full aspect-video bg-cover" 
             style="background-image: url(...)"></div>
        <div class="p-4 flex flex-col gap-3">
            <span class="text-xs font-semibold uppercase ... 
                         bg-primary rounded-full px-3 py-1">
                {{ post.category.name }}
            </span>
            <h3 class="text-lg font-bold">{{ post.title }}</h3>
            <p class="text-sm text-text-secondary-light">
                {{ post.description|default:post.content|truncatewords:30 }}
            </p>
            <p class="text-xs ... border-t ...">
                {{ post.author.username }} • {{ post.created_at|date:"d M Y" }}
            </p>
        </div>
    </div>
    {% endfor %}
</main>
```

**View Logic:**
- Query all published posts ordered by created_at descending
- Separate first post for hero section
- Pass remaining posts to grid
- Apply pagination (10 posts per page including hero)

### 4. Post Detail Page (`templates/blog/post_detail.html`)

**Purpose**: Displays a single blog post with full content and metadata.

**Structure:**

**Header Image:**
```html
<div class="w-full h-64 md:h-96 bg-center bg-cover rounded-xl"
     style="background-image: url(...)"></div>
```

**Article Header:**
```html
<div class="flex flex-col gap-4">
    <h1 class="text-4xl md:text-5xl font-black">{{ post.title }}</h1>
    <p class="text-lg text-text-light-secondary">
        {{ post.description }}
    </p>
</div>
```

**Category/Tag Chips:**
```html
<div class="flex gap-2 py-4 flex-wrap">
    <div class="flex h-7 items-center rounded-full bg-primary/20 px-3">
        <p class="text-primary text-xs font-medium">{{ post.category.name }}</p>
    </div>
    {% for tag in post.tags.all %}
    <div class="flex h-7 items-center rounded-full bg-primary/20 px-3">
        <p class="text-primary text-xs font-medium">{{ tag.name }}</p>
    </div>
    {% endfor %}
</div>
```

**Metadata Bar:**
```html
<div class="flex items-center gap-4 border-y ... py-4 my-4">
    <div class="flex items-center gap-3">
        <div class="rounded-full h-10 w-10 bg-cover"
             style="background-image: url(...)"></div>
        <p class="text-sm font-medium">{{ post.author.username }}</p>
    </div>
    <div class="flex-1 flex gap-x-4">
        <p class="text-sm">{{ post.created_at|date:"M d, Y" }}</p>
        <span>·</span>
        <p class="text-sm">{{ read_time }} min read</p>
    </div>
</div>
```

**Article Content:**
```html
<div class="prose prose-lg dark:prose-invert max-w-none">
    {{ post.content|safe }}
</div>
```

**Related Posts:**
- Display 3 related posts in a grid
- Same card styling as homepage
- Filter by same category or tags

### 5. Category Page (`templates/blog/category_posts.html`)

**Purpose**: Displays all posts in a specific category.

**Structure:**

**Breadcrumbs:**
```html
<div class="flex flex-wrap gap-2">
    <a href="{% url 'blog:post_list' %}">Home</a>
    <span>/</span>
    <a href="#">Blog</a>
    <span>/</span>
    <span>{{ category.name }}</span>
</div>
```

**Page Heading:**
```html
<div class="flex flex-col gap-2">
    <p class="text-4xl sm:text-5xl font-black">{{ category.name }}</p>
    <p class="text-base text-subtle-text-light">
        {{ category.description }}
    </p>
</div>
```

**Post Grid:**
- Same grid layout as homepage (without hero)
- 3-column responsive grid
- Same card styling

### 6. Search Results Page (`templates/blog/search_results.html`)

**Purpose**: Displays search results with a search bar.

**Structure:**

**Search Bar:**
```html
<div class="mb-8">
    <label class="flex flex-col h-14 w-full">
        <div class="flex w-full items-stretch rounded-xl border ...">
            <div class="flex items-center pl-4">
                <span class="material-symbols-outlined">search</span>
            </div>
            <input class="flex-1 ... border-none" 
                   placeholder="Search for articles..." 
                   value="{{ query }}"/>
            <div class="flex items-center pr-4">
                <button>
                    <span class="material-symbols-outlined">close</span>
                </button>
            </div>
        </div>
    </label>
</div>
```

**Results Heading:**
```html
<div class="flex flex-col gap-1 mb-8">
    <h1 class="text-3xl font-black sm:text-4xl">Search Results</h1>
    <p class="text-base">
        Showing {{ posts.count }} results for '{{ query }}'
    </p>
</div>
```

**Results List:**
- Horizontal card layout (flex-row on desktop)
- Image on left (1/3 width), content on right (2/3 width)
- Hover effect with background color change

### 7. Footer (`templates/includes/footer.html`)

**Purpose**: Provides footer navigation and social links.

**Structure:**
```html
<footer class="flex flex-col gap-8 px-5 py-10 text-center 
               border-t ... mt-10">
    <div class="flex flex-wrap items-center justify-center gap-6">
        <a href="#">About</a>
        <a href="#">Privacy Policy</a>
        <a href="#">Contact</a>
    </div>
    <div class="flex justify-center gap-6">
        <a href="#"><svg>Twitter Icon</svg></a>
        <a href="#"><svg>LinkedIn Icon</svg></a>
        <a href="#"><svg>GitHub Icon</svg></a>
    </div>
    <p class="text-sm">© 2024 Modern Blog. All Rights Reserved.</p>
</footer>
```

## Data Models

### Post Model Extension

**New Field:**
```python
class Post(models.Model):
    # ... existing fields ...
    description = models.CharField(
        max_length=300,
        blank=True,
        help_text="Short description of the post (max 300 characters)"
    )
```

**Migration:**
- Add description field as nullable/blank
- No default value needed
- Existing posts will have empty description

**Form Update:**
```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'content', 'category', 
                  'tags', 'featured_image', 'status']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 3,
                'maxlength': 300,
                'placeholder': 'Enter a short description (max 300 characters)'
            }),
            # ... other widgets ...
        }
```

### View Updates

**PostListView:**
```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    posts = context['posts']
    
    if posts:
        context['hero_post'] = posts[0]
        context['remaining_posts'] = posts[1:]
    else:
        context['hero_post'] = None
        context['remaining_posts'] = []
    
    return context
```

**PostDetailView:**
```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    post = context['post']
    
    # Calculate read time (assuming 200 words per minute)
    word_count = len(post.content.split())
    context['read_time'] = max(1, round(word_count / 200))
    
    # Get related posts (same category, exclude current)
    context['related_posts'] = Post.objects.filter(
        category=post.category,
        status='published'
    ).exclude(id=post.id)[:3]
    
    return context
```

## Error Handling

### Missing Featured Images

**Approach**: Use gradient backgrounds as fallbacks

```html
{% if post.featured_image %}
    style="background-image: url('{{ post.featured_image.url }}')"
{% else %}
    style="background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
{% endif %}
```

### Empty Description Field

**Approach**: Fall back to truncated content

```html
{{ post.description|default:post.content|truncatewords:30|striptags }}
```

### No Posts Available

**Approach**: Display empty state message

```html
{% if not posts %}
<div class="flex flex-col items-center justify-center py-20">
    <p class="text-2xl font-bold mb-2">No posts available</p>
    <p class="text-text-secondary-light">Check back later for new content!</p>
</div>
{% endif %}
```

## Testing Strategy

### Visual Testing

1. **Cross-browser Testing**
   - Test in Chrome, Firefox, Safari, Edge
   - Verify Tailwind CSS renders correctly
   - Check dark mode toggle functionality

2. **Responsive Testing**
   - Test on mobile (320px, 375px, 414px)
   - Test on tablet (768px, 1024px)
   - Test on desktop (1280px, 1920px)
   - Verify grid layouts collapse correctly

3. **Component Testing**
   - Verify hero section displays correctly
   - Check post card hover effects
   - Test navigation bar responsiveness
   - Verify footer layout

### Functional Testing

1. **Homepage**
   - Verify hero post displays latest post
   - Check remaining posts exclude hero post
   - Test pagination works correctly
   - Verify empty state when no posts

2. **Post Detail**
   - Check all metadata displays correctly
   - Verify read time calculation
   - Test related posts display
   - Check social share buttons

3. **Category Page**
   - Verify breadcrumbs navigation
   - Check category description displays
   - Test post filtering by category

4. **Search Results**
   - Verify search query displays in input
   - Check results count is accurate
   - Test empty results state

### Database Testing

1. **Description Field**
   - Verify field saves correctly
   - Test max length validation (300 chars)
   - Check blank values are allowed
   - Test migration runs without errors

2. **Existing Data**
   - Verify existing posts display without description
   - Check fallback to truncated content works
   - Test no data loss during migration

## Performance Considerations

### Tailwind CSS

- **CDN Loading**: Using CDN for development/testing
- **Production**: Consider using Tailwind CLI to generate optimized CSS
- **Purging**: Tailwind will automatically purge unused classes in production build

### Image Optimization

- **Lazy Loading**: Add `loading="lazy"` to images below the fold
- **Aspect Ratios**: Use `aspect-video` class to prevent layout shift
- **Responsive Images**: Consider using Django's image processing for different sizes

### Query Optimization

- **Select Related**: Use `select_related('author', 'category')` for post queries
- **Prefetch Related**: Use `prefetch_related('tags')` for tag queries
- **Pagination**: Limit posts per page to 10 for performance

### Caching Strategy

- **Template Fragments**: Cache post cards that don't change frequently
- **Query Results**: Cache category and tag lists
- **Static Assets**: Leverage browser caching for fonts and icons

## Implementation Notes

### Phase 1: Base Setup
1. Update base.html with Tailwind CSS
2. Create new navbar.html include
3. Create new footer.html include
4. Test base template renders correctly

### Phase 2: Database Changes
1. Add description field to Post model
2. Create and run migration
3. Update PostForm to include description
4. Update admin interface

### Phase 3: Homepage
1. Update post_list.html template
2. Modify PostListView context
3. Test hero section and grid layout
4. Verify pagination works

### Phase 4: Post Detail
1. Update post_detail.html template
2. Add read time calculation
3. Add related posts logic
4. Test all components

### Phase 5: Other Pages
1. Update category_posts.html
2. Update search_results.html
3. Update tag_posts.html
4. Test all listing pages

### Phase 6: Polish
1. Add hover effects and transitions
2. Test dark mode (if implementing)
3. Verify responsive behavior
4. Cross-browser testing

## Dependencies

### External Resources

- **Tailwind CSS**: https://cdn.tailwindcss.com (CDN)
- **Google Fonts**: Inter font family
- **Material Symbols**: Icon font for UI elements

### Django Packages

- No new packages required
- Uses existing Django template system
- Uses existing Django ORM

### Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ JavaScript support
- CSS Grid and Flexbox support
- CSS Custom Properties support
