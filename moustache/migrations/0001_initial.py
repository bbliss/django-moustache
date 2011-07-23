# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Babe'
        db.create_table('moustache_babe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('pic1', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('pic2', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('pic3', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('pic4', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('pic5', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('rating', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=1)),
            ('rating_count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('moustache', ['Babe'])


    def backwards(self, orm):
        
        # Deleting model 'Babe'
        db.delete_table('moustache_babe')


    models = {
        'moustache.babe': {
            'Meta': {'object_name': 'Babe'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'pic2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'pic3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'pic4': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'pic5': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '1'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['moustache']
