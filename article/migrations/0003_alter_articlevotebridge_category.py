from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_articlevotebridge_remove_vote_vote_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlevotebridge',
            name='category',
            field=models.CharField(default='', max_length=50, verbose_name='게시글 투표 카테고리 이름'),
        ),
    ]
