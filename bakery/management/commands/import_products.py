from django.core.management.base import BaseCommand
from bakery.models import Category, Product

PRODUCTS_DATA = {
    'Mini-Treats': [
        {'name': 'Gâteau Soirée Box', 'slug': 'gateau-soiree-box', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/401310004/Picture9%20%284%29.png', 'price': 450},
        {'name': 'Gâteau Soirée Medium Box', 'slug': 'gateau-soiree-medium', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/401310006/Picture11%20%282%29.png', 'price': 500},
        {'name': 'Petite Four Medium Box', 'slug': 'petite-four-medium', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/401110017/Picture12%20%282%29.png', 'price': 420},
        {'name': 'Mini Cake Pops Box', 'slug': 'mini-cake-pops', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/40004810/Picture23-min.png', 'price': 400},
        {'name': 'Mini Sablé Box', 'slug': 'mini-sable-box', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/40004945/Picture155-min.png', 'price': 400},
        {'name': 'Mini Brownies Box', 'slug': 'mini-brownies-box', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/400330001/Picture10%20%283%29.png', 'price': 430},
        {'name': 'White Chocolate Tart', 'slug': 'white-chocolate-tart', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/a1f3ab98-2665-4f8e-ae68-b8fea2b69956-638387534041894119.png', 'price': 480},
        {'name': 'Mini Black Forest Tart', 'slug': 'mini-black-forest-tart', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/40009591/Picture7-min%20%281%29.png', 'price': 470},
        {'name': 'Lemon Blueberry Tart', 'slug': 'lemon-blueberry-tart', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/400100059/Picture10%20%284%29.png', 'price': 460},
        {'name': 'Mini Oriental Box', 'slug': 'mini-oriental-box', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/BAO-76908138/Picture9-min%20%281%29.png', 'price': 420},
    ],
    'Savory-Shareable-Boxes': [
        {'name': 'Large Mini Pain Box', 'slug': 'large-mini-pain-box', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/676f74ff-982c-4678-bcc9-a0d166e35ca0-638259784269457327.png', 'price': 580},
        {'name': 'Mini Club Premium Box', 'slug': 'mini-club-premium-box', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/5760cce5-e6a9-4bd9-b893-eb8f61c5f854-638550031958396749.png', 'price': 600},
        {'name': 'Mini Club & Pain Box', 'slug': 'mini-club-pain-box', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/41d0280e-a7c0-496d-aac2-05f3e26f801f-638259790836492472.png', 'price': 550},
        {'name': 'Large Salaison Box', 'slug': 'large-salaison-box', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/40006109/Picture2.png', 'price': 620},
        {'name': 'Party Box', 'slug': 'party-box', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/f8393c84-af75-45ef-a1e4-176b2ce61c19-638259823022384668.png', 'price': 650},
        {'name': 'Premium Sandwich Box', 'slug': 'premium-sandwich-box', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/40006050/Images/Picture13-min.png', 'price': 590},
        {'name': 'Small Mini Club Box', 'slug': 'small-mini-club-box', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/1a033d0d-53a1-47a0-9741-26cee74d1341-638259786041047776.png', 'price': 470},
        {'name': 'Small Mini Pain Box', 'slug': 'small-mini-pain-box', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/4b9f1214-e5df-4611-a63f-92a8e1ebbb06-638259789198565002.png', 'price': 460},
        {'name': 'Sesame Paton Salé Jar', 'slug': 'sesame-paton-sale-jar', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/WKW-06521348/Picture4-min%20%287%29.png', 'price': 440},
        {'name': 'Cumin Paton Salé Jar', 'slug': 'cumin-paton-sale-jar', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/IXK-49427100/Picture8-min%20%281%29.png', 'price': 440},
    ],
    'Salty-Snacks': [
        {'name': 'Small Mini Pain Box', 'slug': 'salty-small-mini-pain', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/4b9f1214-e5df-4611-a63f-92a8e1ebbb06-638259789198565002.png', 'price': 460},
        {'name': 'Small Mini Club Box', 'slug': 'salty-small-mini-club', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/1a033d0d-53a1-47a0-9741-26cee74d1341-638259786041047776.png', 'price': 470},
        {'name': 'Sesame Paton Salé Jar', 'slug': 'salty-sesame-paton', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/WKW-06521348/Picture4-min%20%287%29.png', 'price': 440},
        {'name': 'Black Seed Paton Salé Jar', 'slug': 'black-seed-paton', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/DDI-18285571/Picture1.png', 'price': 450},
        {'name': 'Cumin Paton Salé Jar', 'slug': 'salty-cumin-paton', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/IXK-49427100/Picture8-min%20%281%29.png', 'price': 440},
    ],
    'Ice-Cream-Tortes': [
        {'name': 'Creamy Lotus Ice Cream', 'slug': 'creamy-lotus-ice-cream', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/e2100bce-b52a-42a6-83e5-570a4ac1e610-638360967202049465.png', 'price': 650},
        {'name': 'Pistachio Magic Ice Cream', 'slug': 'pistachio-magic-ice-cream', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/c37f8/601000062/Pistachio%20Mastic%20Ice%20Cream.png', 'price': 700},
        {'name': 'Swiss Roll Ice Cream', 'slug': 'swiss-roll-ice-cream', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/c37f8/601000063/Swiss%20Roll%20Ice%20Cream%20Torte.png', 'price': 680},
        {'name': 'Alaska Ice Cream', 'slug': 'alaska-ice-cream', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/401700050/Picture2%20%284%29.png', 'price': 720},
        {'name': 'Mini Mango Ice Cream', 'slug': 'mini-mango-ice-cream', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/c37f8/401700054/Picture3%20%286%29.png', 'price': 580},
        {'name': 'Oreo Ice Cream', 'slug': 'oreo-ice-cream', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/40008861/Oreo.png', 'price': 620},
    ],
    'Tortes': [
        {'name': 'Half Chocolate Half Mango Torte', 'slug': 'half-choc-half-mango-torte', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/40007241/Picture4-min%20%284%29.png', 'price': 680},
        {'name': 'Four Seasons Torte', 'slug': 'four-seasons-torte', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/5d2d9480-c862-4481-87c5-a82120bcdeb2-638360968194195249.png', 'price': 700},
        {'name': 'Maltesers Chocolate Fudge Torte', 'slug': 'maltesers-chocolate-fudge', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/400300012/ChatGPT%20Image%20Jun%2029%2C%202026%2C%2003_20_54%20PM%20%281%29.png', 'price': 720},
        {'name': 'Choco Lovers Torte', 'slug': 'choco-lovers-torte', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/5d7c67fb-f71f-411a-8225-b993195c990e-638259725993624487.png', 'price': 660},
        {'name': 'Lemon Blueberry Torte', 'slug': 'lemon-blueberry-torte', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/400100059/Picture10%20%284%29.png', 'price': 640},
        {'name': 'Black Forest Torte', 'slug': 'black-forest-torte', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/6c85ca9e-feda-44db-a114-49c25a76ef02-638259714427918300.png', 'price': 680},
    ],
    'Can-Cake': [
        {'name': 'Dubai Chocolate', 'slug': 'dubai-chocolate', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/400310068/Picture17%20%282%29.png', 'price': 550},
        {'name': 'Caramel Mousse', 'slug': 'caramel-mousse', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/400310071/Picture18%20%282%29.png', 'price': 530},
        {'name': 'Panda Cake', 'slug': 'panda-cake', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/401830017/Picture15%20%282%29.png', 'price': 520},
        {'name': 'Krunchoko', 'slug': 'krunchoko', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/400310069/Picture16%20%282%29.png', 'price': 560},
    ],
    'Oriental-Sweets-Boxes': [
        {'name': 'Plain Basbousa', 'slug': 'plain-basbousa', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/7783017b-9e26-4892-85d2-e32b92a16486-638457052120443742.png', 'price': 480},
        {'name': 'Hazelnut Basbousa', 'slug': 'hazelnut-basbousa', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/05de60cd-57dd-48f1-b860-5d92c136dcb8-638457053038495898.png', 'price': 520},
        {'name': 'Oriental Box', 'slug': 'oriental-box', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/400600001/Picture5%20%285%29.png', 'price': 550},
        {'name': 'Premium Oriental Box', 'slug': 'premium-oriental-box', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/400600002/Picture8%20%284%29.png', 'price': 620},
        {'name': 'Imperial Oriental Box', 'slug': 'imperial-oriental-box', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/400600014/Picture7%20%284%29.png', 'price': 680},
        {'name': 'Mixed Oriental Sweets Box', 'slug': 'mixed-oriental-sweets', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/400600021/Images/Picture31-min.png', 'price': 600},
        {'name': 'Mini Oriental Box', 'slug': 'mini-oriental-sweets', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/BAO-76908138/Picture9-min%20%281%29.png', 'price': 420},
    ],
    'Cakes': [
        {'name': 'Almond Cake', 'slug': 'almond-cake', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/ffb41c83-1c4b-44a3-9022-6b30cfdd6f6f-638265804426704623.png', 'price': 600},
        {'name': 'Marble Cake', 'slug': 'marble-cake', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/064baeaf-eef9-41f6-8443-590bafffe213-638558721614878002.png', 'price': 580},
        {'name': 'Christmas Cake', 'slug': 'christmas-cake', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/308e0f8f-4a55-4f38-ba1e-ca0eaa72c3b7-638265803978695884.png', 'price': 650},
        {'name': 'Date Cake', 'slug': 'date-cake', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/400320005/ChatGPT%20Image%20May%2017%2C%202026%2C%2012_21_03%20PM.jpg', 'price': 620},
        {'name': 'Honey English Cake', 'slug': 'honey-english-cake', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/380b8219-9745-4673-ae3c-d817d7b5c890-638363328415512638.png', 'price': 590},
        {'name': 'Lemon Cake', 'slug': 'lemon-cake', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/d84516cc-1928-435e-b545-a995017a907b-638265802775765757.png', 'price': 540},
        {'name': 'Rose Water Cake', 'slug': 'rose-water-cake', 'image': 'https://xretail.blob.core.windows.net/lapoirecontainer/8049b320-c56d-4c72-9bbd-fc62738fd899-638265800919473120.png', 'price': 560},
    ],
    'Sugar-Free': [
        {'name': 'Milk Chocolate Bar Sugar-Free', 'slug': 'milk-chocolate-sf', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/401450042/Picture6%20%284%29.png', 'price': 480},
        {'name': 'Hazelnut Chocolate Bar Sugar-Free', 'slug': 'hazelnut-chocolate-sf', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/401450043/Picture5%20%283%29.png', 'price': 500},
        {'name': 'Dark Chocolate Bar Sugar-Free', 'slug': 'dark-chocolate-sf', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/fa04d/401450044/Picture4%20%283%29.png', 'price': 470},
        {'name': 'Almond Dark Chocolate Bar Sugar-Free', 'slug': 'almond-dark-chocolate-sf', 'image': 'https://xrsm102202001015ss3.lapoire.online/assets/catalog/c37f8/401450045/Picture3%20%284%29.png', 'price': 520},
    ],
}

class Command(BaseCommand):
    help = 'Import all products into the database'

    def handle(self, *args, **options):
        self.stdout.write('Starting product import...')
        for cat_slug, products in PRODUCTS_DATA.items():
            category, created = Category.objects.get_or_create(
                slug=cat_slug,
                defaults={'name': cat_slug.replace('-', ' ').title(), 'is_active': True}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
            for p in products:
                product, created = Product.objects.get_or_create(
                    slug=p['slug'],
                    defaults={
                        'category': category,
                        'name': p['name'],
                        'image_url': p['image'],
                        'price': p['price'],
                        'stock': 20,
                        'description': f'Delicious {p["name"]} from MagdisBakery'
                    }
                )
                if created:
                    self.stdout.write(f'  Created product: {product.name}')
        self.stdout.write(self.style.SUCCESS('✅ Product import completed!'))