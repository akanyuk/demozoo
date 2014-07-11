from django.conf.urls import patterns

urlpatterns = patterns('parties.views',
	(r'^parties/$', 'parties.index', {}, 'parties'),
	(r'^parties/by_date/$', 'parties.by_date', {}, 'parties_by_date'),
	(r'^parties/(\d+)/$', 'parties.show', {}, 'party'),
	(r'^parties/(\d+)/history/$', 'parties.history', {}, 'party_history'),
	(r'^parties/series/(\d+)/$', 'parties.show_series', {}, 'party_series'),
	(r'^parties/series/(\d+)/history/$', 'parties.series_history', {}, 'party_series_history'),
	(r'^parties/series/(\d+)/edit/$', 'parties.edit_series', {}, 'party_edit_series'),
	(r'^parties/series/(\d+)/edit_notes/$', 'parties.edit_series_notes', {}, 'party_edit_series_notes'),
	(r'^parties/new/$', 'parties.create', {}, 'new_party'),
	(r'^parties/(\d+)/add_competition/$', 'parties.add_competition', {}, 'party_add_competition'),
	(r'^parties/(\d+)/edit/$', 'parties.edit', {}, 'edit_party'),
	(r'^parties/(\d+)/edit_competition/(\d+)/$', 'parties.edit_competition', {}, 'party_edit_competition'),
	(r'^parties/(\d+)/edit_notes/$', 'parties.edit_notes', {}, 'party_edit_notes'),
	(r'^parties/(\d+)/edit_external_links/$', 'parties.edit_external_links', {}, 'party_edit_external_links'),
	(r'^parties/(\d+)/results_file/(\d+)/$', 'parties.results_file', {}, 'party_results_file'),
	(r'^parties/autocomplete/$', 'parties.autocomplete', {}),
	(r'^parties/(\d+)/edit_invitations/$', 'parties.edit_invitations', {}, 'party_edit_invitations'),

	(r'^competitions/(\d+)/$', 'competitions.show', {}, 'competition'),
	(r'^competitions/(\d+)/history/$', 'competitions.history', {}, 'competition_history'),
	(r'^competitions/(\d+)/edit$', 'competitions.edit', {}, 'competition_edit'),
	(r'^competitions/(\d+)/import_text$', 'competitions.import_text', {}, 'competition_import_text'),

	(r'^competition_api/add_placing/(\d+)/$', 'competition_api.add_placing', {}),
	(r'^competition_api/update_placing/(\d+)/$', 'competition_api.update_placing', {}),
	(r'^competition_api/delete_placing/(\d+)/$', 'competition_api.delete_placing', {}),
)
