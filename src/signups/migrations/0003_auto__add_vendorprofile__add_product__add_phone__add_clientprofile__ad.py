# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VendorProfile'
        db.create_table(u'signups_vendorprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('payment', self.gf('django.db.models.fields.TextField')(max_length=120)),
        ))
        db.send_create_signal(u'signups', ['VendorProfile'])

        # Adding model 'Product'
        db.create_table(u'signups_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signups.Category'])),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signups.VendorProfile'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('stock', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'signups', ['Product'])

        # Adding model 'Phone'
        db.create_table(u'signups_phone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('phone', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'signups', ['Phone'])

        # Adding model 'ClientProfile'
        db.create_table(u'signups_clientprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal(u'signups', ['ClientProfile'])

        # Adding model 'ProductInOrder'
        db.create_table(u'signups_productinorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signups.Order'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signups.Product'])),
            ('unit_price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'signups', ['ProductInOrder'])

        # Adding model 'ProductImage'
        db.create_table(u'signups_productimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signups.Product'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'signups', ['ProductImage'])

        # Adding model 'Order'
        db.create_table(u'signups_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('purachase_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
        ))
        db.send_create_signal(u'signups', ['Order'])

        # Adding model 'Category'
        db.create_table(u'signups_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal(u'signups', ['Category'])


    def backwards(self, orm):
        # Deleting model 'VendorProfile'
        db.delete_table(u'signups_vendorprofile')

        # Deleting model 'Product'
        db.delete_table(u'signups_product')

        # Deleting model 'Phone'
        db.delete_table(u'signups_phone')

        # Deleting model 'ClientProfile'
        db.delete_table(u'signups_clientprofile')

        # Deleting model 'ProductInOrder'
        db.delete_table(u'signups_productinorder')

        # Deleting model 'ProductImage'
        db.delete_table(u'signups_productimage')

        # Deleting model 'Order'
        db.delete_table(u'signups_order')

        # Deleting model 'Category'
        db.delete_table(u'signups_category')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'signups.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'signups.clientprofile': {
            'Meta': {'object_name': 'ClientProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'signups.order': {
            'Meta': {'object_name': 'Order'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['signups.Product']", 'through': u"orm['signups.ProductInOrder']", 'symmetrical': 'False'}),
            'purachase_date': ('django.db.models.fields.DateTimeField', [], {}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'})
        },
        u'signups.phone': {
            'Meta': {'object_name': 'Phone'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'signups.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signups.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'stock': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signups.VendorProfile']"})
        },
        u'signups.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signups.Product']"})
        },
        u'signups.productinorder': {
            'Meta': {'object_name': 'ProductInOrder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signups.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['signups.Product']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'})
        },
        u'signups.signup': {
            'Meta': {'object_name': 'SignUp'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'for_you': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lname': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'signups.vendorprofile': {
            'Meta': {'object_name': 'VendorProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.TextField', [], {'max_length': '120'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['signups']