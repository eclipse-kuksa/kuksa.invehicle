# Copyright (c) 2019 Eclipse Kuksa project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH

# This file validates the token.

from jose import jwt
import logging


def isTokenValid(token, rsa_key):
    try:
        jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"]
        )
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired")
        return False
    except Exception as exp:
        logging.error("Exception occurred when trying to decode jwt token:", exp)
        return False
    return True


def isTokenValidAud(token, rsa_key, audience):
    try:
        jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"], audience=audience
        )
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired")
        return False
    except Exception as exp:
        logging.error("Exception occurred when trying to decode jwt token with audience parameter set:", exp)
        return False
    return True
