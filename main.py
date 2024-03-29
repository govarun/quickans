'''
 * Copyright 2023 QuickAns
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 '''

import asyncio
import configparser
from graph import Graph

async def main():
    print('Python Graph Tutorial\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    await greet_user(graph)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Display access token')
        print('2. List my inbox')
        print('3. Send mail')
        print('4. Make a Graph call')

        try:
            choice = int(input())
        except ValueError:
            choice = -1

        if choice == 0:
            print('Goodbye...')
        elif choice == 1:
            await display_access_token(graph)
        elif choice == 2:
            await list_inbox(graph)
        elif choice == 3:
            await send_mail(graph)
        elif choice == 4:
            await make_graph_call(graph)
        else:
            print('Invalid choice!\n')


async def greet_user(graph: Graph):
    user = await graph.get_user()
    if user is not None:
        print('Hello,', user.display_name)
        # For Work/school accounts, email is in mail property
        # Personal accounts, email is in userPrincipalName
        print('Email:', user.mail or user.user_principal_name, '\n')

async def display_access_token(graph: Graph):
    token = await graph.get_user_token()
    print('User token:', token, '\n')

async def list_inbox(graph: Graph):
    message_page = await graph.get_inbox()
    if message_page is not None and message_page.value is not None:
        # Output each message's details
        for message in message_page.value:
            print(type(message))
            print("Body:", message.body_preview)
            print('Message:', message.subject)
            if (
                message.from_ is not None and
                message.from_.email_address is not None
            ):
                print('  From:', message.from_.email_address.name or 'NONE')
                print('  From email:', message.from_.email_address.address or 'NONE')
            else:
                print('  From: NONE')
            print('  Status:', 'Read' if message.is_read else 'Unread')
            print('  Received:', message.received_date_time)

        # If @odata.nextLink is present
        more_available = message_page.odata_next_link is not None
        print('\nMore messages available?', more_available, '\n')

async def send_mail(graph: Graph):
    # Send mail to the signed-in user
    # Get the user for their email address
    user = await graph.get_user()
    if user is not None:
        user_email = user.mail or user.user_principal_name

        await graph.send_mail('Testing Microsoft Graph', 'Hello world!', "ssehgal4@illinois.edu" or '')
        print('Mail sent.\n')

async def make_graph_call(graph: Graph):
    # TODO
    return


# Run main
asyncio.run(main())