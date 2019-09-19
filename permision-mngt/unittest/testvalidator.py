# Copyright (c) 2019 Eclipse Kuksa project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH

import unittest
import tokenValidator


class TestValidatorMethods(unittest.TestCase):
    def test_istoken_valid(self):
        test_rsakey = '-----BEGIN PUBLIC KEY-----\n' \
                      'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApdpZcyqLf0L9ySZKvKHW' \
                      '1Vwfk70eFdHqtgIAxFvVaByzrJbbrtnVggNRquJ8S6+A5PqVkDS06Hw8pcS4Jkmz' \
                      'tTRhKmvc2lV+0/jeZ7gKG2da6oQihWBCesvqvL9GnRqh/wqo3dVf4iAzh9a/si09' \
                      'Qylyk26Ip/f/avldSSfdMf3UKE8rJCDsqao9WavXBZwm8NrF2p/RjhfVqKuM6N9i' \
                      'Oq1a2dUV7XNrz6MY02xTjEV65h7h0gZBYEc5U3Dk9Rr49OH9QTXwz0qDgnCMgjyy' \
                      'g152JjCeCI+yZUg5F1CLEjj5NBiWqMikJihEqWt1eCebJKUlrdW18WCasr3A9P1E' \
                      'XwIDAQAB\n' \
                      '-----END PUBLIC KEY-----'
        test_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzd3BPeXZVUGZLc' \
                     '0lhbmhlT0xvQUVyTG4wTDNBOVNLa0pJVXk2aFc4UTd3In0.eyJqdGkiOiIwMmNhZT' \
                     'ZhZS1iZDNkLTQ3NTAtYjAxMS05MWI5ZWM0YTZjNWYiLCJleHAiOjE1Njg3NjcxMTI' \
                     'sIm5iZiI6MCwiaWF0IjoxNTY4NzMxMTEyLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0' \
                     'OjgwODAvYXV0aC9yZWFsbXMvS3Vrc2EiLCJzdWIiOiI4MjA3ZTU5MC1iZjg2LTQ1O' \
                     'WMtOTZkZC0yNGVkYTZmZWRlZDAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJLdWtzYS' \
                     '1kYXNoYm9hcmQiLCJhdXRoX3RpbWUiOjAsInNlc3Npb25fc3RhdGUiOiI5ZTZiZDY' \
                     '3My05NDliLTQ4MmItYWIwZi0wNjBhMDI0ZmE5ZjMiLCJhY3IiOiIxIiwic2NvcGUi' \
                     'OiIiLCJjbGllbnRJZCI6Ikt1a3NhLWRhc2hib2FyZCIsImNsaWVudEhvc3QiOiIxM' \
                     'jcuMC4wLjEiLCJ3M2MtdnNzIjp7IlZlaGljbGUuT0JELkVuZ2luZVNwZWVkIjoid3' \
                     'IifSwiY2xpZW50QWRkcmVzcyI6IjEyNy4wLjAuMSJ9.k7YS1XA71pu0PfBGjIciQu' \
                     'egS90LZeEmKW5Z63dXh7E1l0tbWU3l96FWRD4d3mwISPpUPaUo7LORoPHtQ3LPqTa' \
                     'Z-zmT4MklE8192ZAk86L-Y2NzgHXX_xc4FCsssYAT7Zcu0QlfgB4abxyuCUFlBSl-' \
                     'NMF71ErIjzk8-G_Bz1Tm_OV42yIKXd04AhuTSZ4A1R77lZRAgaPllwNuD3VQ05ELQ' \
                     'Ct2CE3HmLM7QbJjKzgfQKESW3L-8irW8GGMpyYsWk9fM0fIGbpS4iibsu9YmBNbzK' \
                     'RafCrV_jmbDvcz36sDJJHvz_22DdtpJUVqzkBZtx70Jrtdy2tTeie-DNbBPg'
        tokenValidator.isTokenValid(test_Token, test_rsakey)
