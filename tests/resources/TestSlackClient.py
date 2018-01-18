class TestSlackClient(object):
    """
    The TestSlackClient is a test resource for making calls to the Slack API.
    """
    def __init__(self, token):
        self.token = token

    def api_call(self, method, **kwargs):
        if method == 'team.info':
            return {'ok': True,
                    'team': {'id': 'T8TQP6ABE', 'name': 'Clippy Sandbox', 'domain': 'clippy-sandbox',
                             'email_domain': 'solutionloft.com',
                             'icon': {
                                 'image_34': 'https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-01-16/'
                                             '299309939633_9743929b7bd7020465f7_34.png',
                                 'image_44': 'https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-01-16/'
                                             '299309939633_9743929b7bd7020465f7_44.png',
                                 'image_68': 'https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-01-16/'
                                             '299309939633_9743929b7bd7020465f7_68.png',
                                 'image_88': 'https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-01-16/'
                                             '299309939633_9743929b7bd7020465f7_88.png',
                                 'image_102': 'https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-01-16/'
                                              '299309939633_9743929b7bd7020465f7_102.png',
                                 'image_132': 'https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-01-16/'
                                              '299309939633_9743929b7bd7020465f7_132.png',
                                 'image_230': 'https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-01-16/'
                                              '299309939633_9743929b7bd7020465f7_230.png',
                                 'image_original': 'https://slack-files2.s3-us-west-2.amazonaws.com/avatars/'
                                                   '2018-01-16/299309939633_9743929b7bd7020465f7_original.png'}}}
        elif method == 'users.info':
            return {'ok': True,
                    'user': {'id': 'U8USTVANB', 'team_id': 'T8TQP6ABE', 'name': 'will', 'deleted': False,
                             'color': '9f69e7', 'real_name': 'Will Fry', 'tz': 'America/Los_Angeles',
                             'tz_label': 'Pacific Standard Time', 'tz_offset': -28800,
                             'profile': {'real_name': 'Will Fry', 'display_name': '', 'avatar_hash': 'g6864d4e3130',
                                         'real_name_normalized': 'Will Fry', 'display_name_normalized': '',
                                         'image_24': 'https://secure.gravatar.com/avatar/'
                                                     '6864d4e3130f87c06890a4dc31cecd92.jpg'
                                                     '?s=24&d=https%3A%2F%2Fa.slack-edge.com'
                                                     '%2F66f9%2Fimg%2Favatars%2Fava_0000-24.png',
                                         'image_32': 'https://secure.gravatar.com/avatar/'
                                                     '6864d4e3130f87c06890a4dc31cecd92.jpg'
                                                     '?s=32&d=https%3A%2F%2Fa.slack-edge.com'
                                                     '%2F66f9%2Fimg%2Favatars%2Fava_0000-32.png',
                                         'image_48': 'https://secure.gravatar.com/avatar/'
                                                     '6864d4e3130f87c06890a4dc31cecd92.jpg'
                                                     '?s=48&d=https%3A%2F%2Fa.slack-edge.com'
                                                     '%2F66f9%2Fimg%2Favatars%2Fava_0000-48.png',
                                         'image_72': 'https://secure.gravatar.com/avatar/'
                                                     '6864d4e3130f87c06890a4dc31cecd92.jpg'
                                                     '?s=72&d=https%3A%2F%2Fa.slack-edge.com'
                                                     '%2F66f9%2Fimg%2Favatars%2Fava_0000-72.png',
                                         'image_192': 'https://secure.gravatar.com/avatar/'
                                                      '6864d4e3130f87c06890a4dc31cecd92.jpg'
                                                      '?s=192&d=https%3A%2F%2Fa.slack-edge.com'
                                                      '%2F7fa9%2Fimg%2Favatars%2Fava_0000-192.png',
                                         'image_512': 'https://secure.gravatar.com/avatar/'
                                                      '6864d4e3130f87c06890a4dc31cecd92.jpg'
                                                      '?s=512&d=https%3A%2F%2Fa.slack-edge.com'
                                                      '%2F7fa9%2Fimg%2Favatars%2Fava_0000-512.png',
                                         'team': 'T8TQP6ABE'},
                             'is_admin': True, 'is_owner': True, 'is_primary_owner': True,
                             'is_restricted': False, 'is_ultra_restricted': False, 'is_bot': False,
                             'updated': 1516139189, 'is_app_user': False, 'has_2fa': False}}
        else:
            return {'ok': False, 'error': 'unknown_method', 'req_method': method}
