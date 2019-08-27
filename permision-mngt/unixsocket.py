# Copyright (c) 2019 Eclipse Kuksa project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH
# This file handles the unix socket connection.

import socket
import os
import requestHandler

socket_owner = 'kuksa w3c-visserver'
server_address = '/home/pratheek/socket/kuksa_w3c_perm_management'
message_bytes = 1024


def createW3Csocket():
    try:
        os.unlink(server_address)
    except OSError:
        if os.path.exists(server_address):
            raise

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Bind the socket to the address
    print('starting up on {}'.format(server_address))
    #sock.close()
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print('Wait for {} to connect'.format(socket_owner))
        connection, client_address = sock.accept()
        try:
            print('Api connected from ', client_address)

            while True:
                data = connection.recv(message_bytes)  # blocking call will read at most 'message_byte' number of bytes.
                if data:
                    print('received message = {!r}'.format(data))
                    request = data.decode("utf-8")
                    response = requestHandler.processRequest(request)
                    connection.sendall(bytearray(response))
                    connection.close()
                    break
                else:
                    print('no data from {} could be that the connection is closed.'.format(client_address))
                    break
        except Exception as error:
            print("Some error occurred while handling socket connection {}".format(error))
        finally:
            # Clean up the connection
            connection.close()
