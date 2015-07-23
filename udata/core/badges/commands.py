# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from os.path import exists

from udata.commands import submanager
from udata.models import Organization, OrganizationBadge

log = logging.getLogger(__name__)


m = submanager(
    'badges',
    help='Badges related operations',
    description='Handle all badges related operations and maintenance'
)


def toggle_badge(id_or_slug, badge_kind):
    organization = Organization.objects.get_by_id_or_slug(id_or_slug)
    if not organization:
        log.error('No organization found for %s', id_or_slug)
        return
    log.info('Toggling badge {kind} for organization {org}'.format(
        kind=badge_kind,
        org=organization.name
    ))
    existed = False
    for badge in organization.badges:
        if badge.kind == badge_kind:
            organization.badges.remove(badge)
            existed = True
            break
    if not existed:
        badge = OrganizationBadge(kind=badge_kind)
        organization.badges.append(badge)
    organization.save()


@m.command
def toggle(path_or_id, badge_kind):
    '''Toggle a `badge_kind` for a given `path_or_id`

    The `path_or_id` is either an id, a slug or a file containing a list
    of ids or slugs.
    '''
    if exists(path_or_id):
        with open(path_or_id) as open_file:
            for id_or_slug in open_file.readlines():
                toggle_badge(id_or_slug.strip(), badge_kind)
    else:
        toggle_badge(path_or_id, badge_kind)
