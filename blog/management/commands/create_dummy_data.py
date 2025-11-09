"""
Management command to create dummy blog data for testing the UI design.
Usage: python manage.py create_dummy_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Creates dummy blog data for testing the UI design'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating dummy data...')

        # Create test user if doesn't exist
        user, created = User.objects.get_or_create(
            username='testauthor',
            defaults={
                'email': 'author@example.com',
                'first_name': 'Test',
                'last_name': 'Author'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            # Create profile
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'author', 'bio': 'A passionate writer and blogger.'}
            )
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))

        # Create categories
        categories_data = [
            {'name': 'Technology', 'description': 'Latest tech trends, gadgets, and innovations'},
            {'name': 'Design', 'description': 'UI/UX design, web design, and creative inspiration'},
            {'name': 'Development', 'description': 'Programming tutorials, best practices, and code tips'},
            {'name': 'Productivity', 'description': 'Tips and tools to boost your productivity'},
            {'name': 'Business', 'description': 'Entrepreneurship, startups, and business strategies'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Create tags
        tags_data = ['Python', 'JavaScript', 'React', 'Django', 'CSS', 'HTML', 
                     'UI/UX', 'Tutorial', 'Tips', 'Best Practices', 'Web Development',
                     'Mobile', 'API', 'Database', 'Security']

        tags = {}
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags[tag_name] = tag
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created tag: {tag.name}'))

        # Create posts
        posts_data = [
            {
                'title': 'The Future of Minimalist Design in Digital Products',
                'description': 'Discover how whitespace and clean typography can transform user experiences and bring clarity to your digital products.',
                'content': '''<h2>Introduction</h2>
<p>In a world saturated with information and complex interfaces, minimalism has emerged not just as an aesthetic choice, but as a powerful principle for creating effective and user-friendly digital experiences.</p>

<h2>The Core Principles</h2>
<p>Minimalist design is built on a few fundamental ideas. The most famous is perhaps "less is more." This means every element on the screen must have a purpose.</p>

<ul>
<li><strong>Intentionality:</strong> Every button, line, and piece of text serves a clear function.</li>
<li><strong>Whitespace:</strong> Generous use of negative space to create breathing room and guide the user's eye.</li>
<li><strong>Limited Color Palette:</strong> Often monochromatic or uses a very restricted set of colors to create harmony.</li>
</ul>

<blockquote>
<p>"Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away." - Antoine de Saint-Exupéry</p>
</blockquote>

<h2>Putting It Into Practice</h2>
<p>Adopting minimalism requires a disciplined approach. Start by defining the primary goal of your interface. For a blog post like this one, the goal is readability.</p>

<p>Ultimately, minimalist design is not about making things empty; it's about making them more effective by focusing on what truly matters.</p>''',
                'category': 'Design',
                'tags': ['UI/UX', 'Design', 'Best Practices'],
                'status': 'published'
            },
            {
                'title': '10 Essential Typography Tips for Web Designers',
                'description': 'Elevate your designs with these fundamental typography rules that enhance readability and aesthetic appeal.',
                'content': '''<h2>Why Typography Matters</h2>
<p>Typography is the foundation of good design. It's not just about choosing pretty fonts—it's about creating hierarchy, improving readability, and guiding users through your content.</p>

<h2>The Essential Tips</h2>
<ol>
<li><strong>Choose the Right Font Pairing:</strong> Combine a serif with a sans-serif for contrast.</li>
<li><strong>Establish Visual Hierarchy:</strong> Use size, weight, and spacing to guide the eye.</li>
<li><strong>Mind Your Line Length:</strong> Aim for 50-75 characters per line for optimal readability.</li>
<li><strong>Use Proper Line Height:</strong> Set line-height to 1.5-1.6 for body text.</li>
<li><strong>Limit Font Families:</strong> Stick to 2-3 font families maximum.</li>
</ol>

<p>These principles will help you create more professional and readable designs that users will love.</p>''',
                'category': 'Design',
                'tags': ['Typography', 'Design', 'Tutorial'],
                'status': 'published'
            },
            {
                'title': 'Building Modern Web Apps with Django and React',
                'description': 'A comprehensive guide to creating full-stack applications using Django REST Framework and React.',
                'content': '''<h2>Getting Started</h2>
<p>Combining Django's powerful backend with React's dynamic frontend creates a robust full-stack solution for modern web applications.</p>

<h2>Setting Up Your Environment</h2>
<p>First, you'll need to set up both Django and React. We'll use Django REST Framework to create our API endpoints.</p>

<pre><code>pip install django djangorestframework
npx create-react-app frontend</code></pre>

<h2>Creating the API</h2>
<p>Django REST Framework makes it easy to create RESTful APIs. Start by defining your models, then create serializers and viewsets.</p>

<h2>Connecting React</h2>
<p>Use axios or fetch to connect your React frontend to the Django backend. Handle authentication with JWT tokens for a secure connection.</p>''',
                'category': 'Development',
                'tags': ['Django', 'React', 'Python', 'JavaScript', 'Tutorial'],
                'status': 'published'
            },
            {
                'title': 'The Art of Subtle Animations in UI Design',
                'description': 'Learn how to use animations to guide users and provide meaningful feedback without being distracting.',
                'content': '''<h2>Why Animations Matter</h2>
<p>Animations in UI design serve a purpose beyond aesthetics. They provide feedback, guide attention, and create a sense of continuity in your interface.</p>

<h2>Types of UI Animations</h2>
<ul>
<li><strong>Micro-interactions:</strong> Small animations that respond to user actions</li>
<li><strong>Loading States:</strong> Animations that indicate progress</li>
<li><strong>Transitions:</strong> Smooth changes between states</li>
<li><strong>Attention Seekers:</strong> Animations that draw focus to important elements</li>
</ul>

<h2>Best Practices</h2>
<p>Keep animations subtle and purposeful. They should enhance the user experience, not distract from it. Aim for durations between 200-500ms for most UI animations.</p>''',
                'category': 'Design',
                'tags': ['UI/UX', 'CSS', 'Tutorial'],
                'status': 'published'
            },
            {
                'title': 'Mastering the Pomodoro Technique for Better Focus',
                'description': 'Discover how this simple time management method can dramatically improve your productivity and focus.',
                'content': '''<h2>What is the Pomodoro Technique?</h2>
<p>The Pomodoro Technique is a time management method that uses a timer to break work into focused intervals, traditionally 25 minutes in length, separated by short breaks.</p>

<h2>How It Works</h2>
<ol>
<li>Choose a task to work on</li>
<li>Set a timer for 25 minutes</li>
<li>Work on the task until the timer rings</li>
<li>Take a 5-minute break</li>
<li>After 4 pomodoros, take a longer 15-30 minute break</li>
</ol>

<h2>Benefits</h2>
<p>This technique helps maintain focus, prevents burnout, and provides a sense of accomplishment as you complete each pomodoro.</p>''',
                'category': 'Productivity',
                'tags': ['Productivity', 'Tips', 'Best Practices'],
                'status': 'published'
            },
            {
                'title': 'Understanding RESTful API Design Principles',
                'description': 'A deep dive into REST architecture and how to design clean, maintainable APIs.',
                'content': '''<h2>What is REST?</h2>
<p>REST (Representational State Transfer) is an architectural style for designing networked applications. It relies on stateless, client-server communication.</p>

<h2>Key Principles</h2>
<ul>
<li><strong>Stateless:</strong> Each request contains all information needed to process it</li>
<li><strong>Client-Server:</strong> Separation of concerns between UI and data storage</li>
<li><strong>Cacheable:</strong> Responses must define themselves as cacheable or not</li>
<li><strong>Uniform Interface:</strong> Consistent way to interact with resources</li>
</ul>

<h2>HTTP Methods</h2>
<p>Use GET for reading, POST for creating, PUT/PATCH for updating, and DELETE for removing resources.</p>''',
                'category': 'Development',
                'tags': ['API', 'Tutorial', 'Best Practices', 'Web Development'],
                'status': 'published'
            },
            {
                'title': 'CSS Grid vs Flexbox: When to Use Each',
                'description': 'Understanding the differences between CSS Grid and Flexbox to choose the right tool for your layout needs.',
                'content': '''<h2>Introduction</h2>
<p>Both CSS Grid and Flexbox are powerful layout tools, but they excel in different scenarios. Understanding when to use each will make you a more effective developer.</p>

<h2>Flexbox: One-Dimensional Layouts</h2>
<p>Flexbox is designed for laying out items in a single direction—either as a row or a column. It's perfect for navigation bars, card layouts, and centering content.</p>

<h2>CSS Grid: Two-Dimensional Layouts</h2>
<p>Grid is designed for two-dimensional layouts where you need to control both rows and columns simultaneously. It's ideal for page layouts, image galleries, and complex designs.</p>

<h2>When to Use What</h2>
<p>Use Flexbox for components and small-scale layouts. Use Grid for page-level layouts and when you need precise control over both dimensions.</p>''',
                'category': 'Development',
                'tags': ['CSS', 'HTML', 'Tutorial', 'Web Development'],
                'status': 'published'
            },
            {
                'title': 'Building a Personal Brand as a Developer',
                'description': 'Strategies for establishing your online presence and standing out in the tech industry.',
                'content': '''<h2>Why Personal Branding Matters</h2>
<p>In today's competitive tech landscape, having a strong personal brand can open doors to new opportunities, collaborations, and career growth.</p>

<h2>Key Strategies</h2>
<ul>
<li><strong>Create Content:</strong> Write blog posts, create tutorials, or make videos</li>
<li><strong>Be Consistent:</strong> Maintain a regular posting schedule</li>
<li><strong>Engage with Community:</strong> Participate in discussions and help others</li>
<li><strong>Showcase Your Work:</strong> Build a portfolio of your best projects</li>
</ul>

<h2>Getting Started</h2>
<p>Start small. Pick one platform and focus on providing value to your audience. Authenticity is more important than perfection.</p>''',
                'category': 'Business',
                'tags': ['Business', 'Tips', 'Best Practices'],
                'status': 'published'
            },
            {
                'title': 'Introduction to Python Decorators',
                'description': 'Learn how to use Python decorators to write cleaner, more maintainable code.',
                'content': '''<h2>What are Decorators?</h2>
<p>Decorators are a powerful feature in Python that allow you to modify or enhance functions and methods without changing their source code.</p>

<h2>Basic Syntax</h2>
<pre><code>@decorator
def my_function():
    pass</code></pre>

<h2>Common Use Cases</h2>
<ul>
<li>Logging function calls</li>
<li>Measuring execution time</li>
<li>Authentication and authorization</li>
<li>Caching results</li>
</ul>

<h2>Creating Your Own Decorator</h2>
<p>Decorators are just functions that take a function as an argument and return a new function. Understanding this concept is key to mastering decorators.</p>''',
                'category': 'Development',
                'tags': ['Python', 'Tutorial', 'Best Practices'],
                'status': 'published'
            },
            {
                'title': 'Effective Code Review Practices',
                'description': 'Best practices for conducting and receiving code reviews that improve code quality and team collaboration.',
                'content': '''<h2>The Importance of Code Reviews</h2>
<p>Code reviews are essential for maintaining code quality, sharing knowledge, and catching bugs before they reach production.</p>

<h2>For Reviewers</h2>
<ul>
<li>Be constructive and specific in your feedback</li>
<li>Focus on the code, not the person</li>
<li>Ask questions rather than making demands</li>
<li>Acknowledge good work</li>
</ul>

<h2>For Authors</h2>
<ul>
<li>Keep pull requests small and focused</li>
<li>Provide context in your description</li>
<li>Be open to feedback</li>
<li>Respond to all comments</li>
</ul>

<h2>Creating a Positive Culture</h2>
<p>Code reviews should be a learning opportunity for everyone involved. Foster an environment where feedback is welcomed and appreciated.</p>''',
                'category': 'Development',
                'tags': ['Best Practices', 'Tips'],
                'status': 'published'
            },
        ]

        for post_data in posts_data:
            # Check if post already exists
            if Post.objects.filter(title=post_data['title']).exists():
                self.stdout.write(self.style.WARNING(f'Post already exists: {post_data["title"]}'))
                continue

            # Create post
            post = Post.objects.create(
                title=post_data['title'],
                description=post_data['description'],
                content=post_data['content'],
                author=user,
                category=categories[post_data['category']],
                status=post_data['status']
            )

            # Add tags
            for tag_name in post_data['tags']:
                if tag_name in tags:
                    post.tags.add(tags[tag_name])

            post.save()
            self.stdout.write(self.style.SUCCESS(f'Created post: {post.title}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Dummy data created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created {Post.objects.count()} posts'))
        self.stdout.write(self.style.SUCCESS(f'Created {Category.objects.count()} categories'))
        self.stdout.write(self.style.SUCCESS(f'Created {Tag.objects.count()} tags'))
        self.stdout.write(self.style.SUCCESS('\nYou can now view your blog at http://localhost:8000/'))
