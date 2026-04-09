from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from modelcluster.fields import ParentalKey


class ServiceBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.TextBlock()

    class Meta:
        icon = 'doc-full'


class HomePage(Page):
    hero_headline = models.CharField(max_length=100, default="SEE THE TRENDS.")
    hero_subheadline = models.CharField(max_length=100, default="SHAPE THE FUTURE.")
    hero_body = models.TextField(
        default="Specializing in data engineering and analytics, we help businesses organize and explore their data for better decision-making."
    )
    services = StreamField([('service', ServiceBlock())], blank=True, use_json_field=True)
    cta_headline = models.CharField(max_length=200, default="Start Your Data Transformation")
    cta_subheading = models.CharField(
        max_length=300,
        default="See how better data can drive better results—let's talk."
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_headline'),
            FieldPanel('hero_subheadline'),
            FieldPanel('hero_body'),
        ], heading="Hero Section"),
        FieldPanel('services'),
        MultiFieldPanel([
            FieldPanel('cta_headline'),
            FieldPanel('cta_subheading'),
        ], heading="CTA Section"),
    ]

    class Meta:
        verbose_name = "Home Page"


class ForAgenciesPage(Page):
    hero_headline = models.CharField(max_length=200, default="Scale Your Analytics.")
    hero_subheadline = models.CharField(max_length=200, default="No Overhead. No Contracts.")
    hero_body = models.TextField(
        default="We offer white-labeled data solutions for agencies covering Google Analytics, Google Tag Manager, and Adobe Analytics management with flexible account scaling."
    )
    feature_headline = models.CharField(max_length=200, default="Fully Managed Dashboards, Ready for Your Clients")
    feature_body = models.TextField(
        default="Custom dashboard creation across platforms (Power BI, Looker Studio, Tableau) with data integration, automation, and branding."
    )
    secondary_headline = models.CharField(max_length=200, default="Scalable. Seamless. Yours.")
    secondary_body = models.TextField(
        default="Our managed analytics services adapt to your agency's growth—add or remove accounts with no long-term commitment."
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_headline'),
            FieldPanel('hero_subheadline'),
            FieldPanel('hero_body'),
        ], heading="Hero Section"),
        MultiFieldPanel([
            FieldPanel('feature_headline'),
            FieldPanel('feature_body'),
        ], heading="Feature Section"),
        MultiFieldPanel([
            FieldPanel('secondary_headline'),
            FieldPanel('secondary_body'),
        ], heading="Secondary Feature Section"),
    ]

    class Meta:
        verbose_name = "For Agencies Page"


class ForBusinessesPage(Page):
    hero_headline = models.CharField(max_length=200, default="Streamline Your Data.")
    hero_subheadline = models.CharField(max_length=200, default="Automate Your Reports.")
    hero_body = models.TextField(
        default="We help businesses eliminate spreadsheet dependency by automating reporting processes, constructing scalable data infrastructure, and developing interactive dashboards. Our data engineering expertise ensures information is properly organized and continuously refreshed without requiring manual intervention."
    )
    feature_headline = models.CharField(max_length=200, default="Building Your Data Foundation")
    feature_body = models.TextField(
        default="For organizations still using spreadsheets or disorganized data systems, we provide streamlined, automated mechanisms for data collection, storage, and visualization—enabling you to obtain necessary insights without technical complexity or expanding skill requirements."
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_headline'),
            FieldPanel('hero_subheadline'),
            FieldPanel('hero_body'),
        ], heading="Hero Section"),
        MultiFieldPanel([
            FieldPanel('feature_headline'),
            FieldPanel('feature_body'),
        ], heading="Feature Section"),
    ]

    class Meta:
        verbose_name = "For Businesses Page"


class ContactFormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name='form_fields')


class ContactPage(AbstractEmailForm):
    contact_phone = models.CharField(max_length=30, default="502-319-0546")
    contact_email = models.EmailField(default="zrichardson@rich360.io")
    thank_you_text = models.CharField(max_length=300, default="Thank you for your response.")

    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel([
            FieldPanel('contact_phone'),
            FieldPanel('contact_email'),
        ], heading="Contact Information"),
        InlinePanel('form_fields', label="Form Fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldPanel('to_address'),
            FieldPanel('from_address'),
            FieldPanel('subject'),
        ], heading="Email Settings"),
    ]

    def get_form_fields(self):
        return self.form_fields.all()

    class Meta:
        verbose_name = "Contact Page"
