"""
Bootstrap the Rich360 Digital Wagtail site with all pages and content.
Run with: python manage.py setup_site
"""
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import (
    HomePage, ForAgenciesPage, ForBusinessesPage,
    ContactPage, ContactFormField
)


class Command(BaseCommand):
    help = 'Set up the Rich360 Digital site with initial pages'

    def handle(self, *args, **options):
        # Remove the default welcome page and set up root
        root = Page.objects.filter(depth=1).first()
        if root is None:
            self.stderr.write("No root page found.")
            return

        # Delete existing children of root (the default Wagtail welcome page)
        for child in root.get_children():
            if child.slug != 'home' or not HomePage.objects.filter(pk=child.pk).exists():
                child.delete()

        # Create or get HomePage
        if HomePage.objects.exists():
            home = HomePage.objects.first()
            self.stdout.write("HomePage already exists, updating...")
        else:
            home = HomePage(
                title="Rich360 Digital",
                slug="home",
                hero_headline="SEE THE TRENDS.",
                hero_subheadline="SHAPE THE FUTURE.",
                hero_body="Specializing in data engineering and analytics, we help businesses organize and explore their data for better decision-making.",
                cta_headline="Start Your Data Transformation",
                cta_subheading="See how better data can drive better results—let's talk.",
                services=[
                    ('service', {
                        'title': 'Data Engineering',
                        'description': "Our data engineering services create robust architectures and pipelines to efficiently manage, process, and store data, ensuring it's ready for seamless analysis and decision-making.",
                    }),
                    ('service', {
                        'title': 'Data Visualization',
                        'description': "Our data visualization and dashboard services transforms complex data into clear, interactive visuals, making it easier to understand insights and communicate them effectively.",
                    }),
                    ('service', {
                        'title': 'Data Analysis',
                        'description': "Our data analytics service helps uncover meaningful trends, patterns, and insights from large datasets, providing the foundation for data-driven business strategies.",
                    }),
                ],
            )
            root.add_child(instance=home)
            self.stdout.write(self.style.SUCCESS("Created HomePage"))

        # Set up Wagtail Site
        site, created = Site.objects.get_or_create(
            hostname='localhost',
            defaults={
                'root_page': home,
                'site_name': 'Rich360 Digital',
                'port': 8000,
                'is_default_site': True,
            }
        )
        if not created:
            site.root_page = home
            site.site_name = 'Rich360 Digital'
            site.is_default_site = True
            site.save()
        self.stdout.write(self.style.SUCCESS("Site configured"))

        # For Agencies page
        if not ForAgenciesPage.objects.exists():
            agencies = ForAgenciesPage(
                title="For Agencies",
                slug="for-agencies",
                hero_headline="Scale Your Analytics.",
                hero_subheadline="No Overhead. No Contracts.",
                hero_body="We offer white-labeled data solutions for agencies covering Google Analytics, Google Tag Manager, and Adobe Analytics management with flexible account scaling.",
                feature_headline="Fully Managed Dashboards, Ready for Your Clients",
                feature_body="Custom dashboard creation across platforms (Power BI, Looker Studio, Tableau) with data integration, automation, and branding tailored to your agency.",
                secondary_headline="Scalable. Seamless. Yours.",
                secondary_body="Our managed analytics services adapt to your agency's growth—add or remove accounts with no long-term commitment.",
            )
            home.add_child(instance=agencies)
            self.stdout.write(self.style.SUCCESS("Created ForAgenciesPage"))

        # For Businesses page
        if not ForBusinessesPage.objects.exists():
            businesses = ForBusinessesPage(
                title="For Businesses",
                slug="for-businesses",
                hero_headline="Streamline Your Data.",
                hero_subheadline="Automate Your Reports.",
                hero_body="We help businesses eliminate spreadsheet dependency by automating reporting processes, constructing scalable data infrastructure, and developing interactive dashboards. Our data engineering expertise ensures information is properly organized and continuously refreshed without requiring manual intervention.",
                feature_headline="Building Your Data Foundation",
                feature_body="For organizations still using spreadsheets or disorganized data systems, we provide streamlined, automated mechanisms for data collection, storage, and visualization—enabling you to obtain necessary insights without technical complexity or expanding skill requirements.",
            )
            home.add_child(instance=businesses)
            self.stdout.write(self.style.SUCCESS("Created ForBusinessesPage"))

        # Contact page
        if not ContactPage.objects.exists():
            contact = ContactPage(
                title="Contact",
                slug="contact",
                contact_phone="502-319-0546",
                contact_email="zrichardson@rich360.io",
                thank_you_text="Thank you for your response. We'll be in touch within one business day.",
                to_address="zrichardson@rich360.io",
                from_address="noreply@rich360.io",
                subject="New inquiry from Rich360 Digital website",
            )
            home.add_child(instance=contact)
            # Add form fields
            ContactFormField.objects.create(
                page=contact, sort_order=1,
                label="Name", field_type="singleline", required=True,
            )
            ContactFormField.objects.create(
                page=contact, sort_order=2,
                label="Email", field_type="email", required=True,
            )
            ContactFormField.objects.create(
                page=contact, sort_order=3,
                label="How Can We Help?", field_type="multiline", required=False,
            )
            self.stdout.write(self.style.SUCCESS("Created ContactPage with form fields"))

        self.stdout.write(self.style.SUCCESS("\nSite setup complete! Visit http://localhost:8000"))
        self.stdout.write("Admin: http://localhost:8000/admin/  |  user: admin  |  pass: rich360admin")
