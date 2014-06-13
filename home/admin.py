from django.contrib import admin
import models as fmo

admin.site.register( fmo.User )
admin.site.register( fmo.Fidentity )
admin.site.register( fmo.Artist )
admin.site.register( fmo.Venue )
admin.site.register( fmo.Event )
admin.site.register( fmo.Sponsor )
admin.site.register( fmo.VenueType )
admin.site.register( fmo.EventType )
admin.site.register( fmo.Price )
admin.site.register( fmo.PriceCategory )
admin.site.register( fmo.Picture )
admin.site.register( fmo.Geocoordinates )
