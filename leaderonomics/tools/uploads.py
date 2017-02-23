# -*- coding: utf-8 -*-

import os
import uuid

__author__ = 'Yevhenii Onoshko'


def generate_uuid_file_path(filename):
    """
    Helper tool to generate unique path for files
    """
    ext = filename.split('.')[-1]
    filename = '{filename}.{ext}'.format(filename=uuid.uuid4(), ext=ext)
    return "{}/{}/{}".format(filename[:1], filename[2:3], filename)

def get_article_upload_path(instance, filename):
    return 'article/images/{}'.format(generate_uuid_file_path(filename))

def get_avatar_upload_path(instance, filename):
    return 'users/avatars/{}'.format(generate_uuid_file_path(filename))

def get_video_upload_path(instance, filename):
    return 'videos/{}'.format(generate_uuid_file_path(filename))

def get_podcast_upload_path(instance, filename):
    return 'podcast/{}'.format(generate_uuid_file_path(filename))
