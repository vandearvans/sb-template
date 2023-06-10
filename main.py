import discord
import os
import requests
import discord
from discord.ext import commands
from datetime import datetime

import json
import subprocess

import random
import time
from discord.ext import commands
import colorama
from colorama import Fore
import asyncio
from webserver import keep_alive
from pystyle import Colors, Colorate
import pytz

from discord_webhook import DiscordWebhook
import io

import urllib.parse

from blockcypher import get_address_full

import sys

#-----------------------------------------

token = ""
prefix = "e!"
webhook_url = ""
bot = commands.Bot(command_prefix=prefix,
                   help_command=None,
                   case_insensitive=True,
                   self_bot=True)




#-------------Whois V2

#-------------Add time
@bot.command()
async def addtime(ctx, hours: float):
    current_time = time.time()
    current_time = int(current_time)
    seconds = int(hours * 3600)
    future_time = current_time + seconds

    # Convert the resulting time to a string
    result_str = str(future_time)

    await ctx.send(f"The future time is: <t:{result_str}:F>")


#---------------------------Command logger to Console
@bot.event
async def on_command(ctx):
    message = ctx.message.content.split(" ", 1)[1] if len(ctx.message.content.split(" ")) > 1 else "" # Get the message after the command if it exists
    output = f"Command used - {ctx.command.name} {message}".replace('"', '') # Remove quotes from output
    print(Colorate.Horizontal(Colors.blue_to_cyan, output, 1))


#-----Transcript redirect

@bot.command()
async def satrans(ctx, message):
    transcript_url = f"{message}\nTranscript redirect: https://logs.scammeralert.org/view/?url={message}"
    await ctx.send(transcript_url)
    await ctx.message.delete()


#-----------Scammeralert Donations

@bot.command()
async def sadonator(ctx, user: discord.Member, crypto_name: str, transaction_id: str):
    transaction_url = f"https://live.blockcypher.com/{crypto_name.lower()}/tx/{transaction_id}"
    donation_message = f"**Donation**\n> Donator Badge to : {user.mention} | {user.id}\n> Crypto Name : {crypto_name}\n> Transaction Hash : {transaction_id}\n> Transaction Redirect : {transaction_url}\n || <@&888763368943534101> ||"
    await ctx.send(donation_message)
    await ctx.message.delete()




#------------------------------Activity command/AFK

@bot.command()
async def activity(ctx, *, message):
    await bot.change_presence(activity=discord.Game(name=message))
    await ctx.message.delete()
    await ctx.send(f'> **Changed activity to** : `{message}`')

  

#---------------------------Ask Proofs after doing +get for Vouches which are to be proven by the User

@bot.command()
async def vouchverifyog(ctx):
        await ctx.message.delete()
        message = f" To claim those vouches, you gotta prove they're yours. So, make sure to provide legit payment proofs that match the vouch IDs mentioned on the payment app. You got 12 hours to do this. Important points:\n\n> Valid payment proofs required\n> Vouch IDs must match those on the payment app\n> 12-hour deadline\n\nHope that's clear enough!"
        await ctx.send(message)


@bot.command()
async def vouchverify(ctx):
    await ctx.message.delete()
    messages = [
        "To claim those vouches, you gotta prove they're yours. So, make sure to provide legit payment proofs that match the vouch IDs mentioned on the payment app. You got 12 hours to do this. Important points:\n\n> Valid payment proofs required\n> Vouch IDs must match those on the payment app\n\n> 12-hour deadline\n\nHope that's clear enough!",
        "To validate and redeem your vouches, it's necessary to verify their ownership. Kindly submit authentic payment evidence that corresponds to the vouch IDs specified on the payment application within a 12-hour timeframe. Take note of the following important points:\n\n> Please provide valid payment proofs\n> Ensure that the vouch IDs match those on the payment app\n\n> The deadline for submission is 12 hours",
        "To access your vouches, it's important to confirm their authenticity. Please provide verifiable payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Keep in mind the following key points:\n\n> Make sure your payment proofs are valid\n> The vouch IDs should match those on the payment app\n\n> You have a 12-hour deadline to complete this task",
        "To claim your vouches, you must prove that they belong to you. Please submit valid payment proofs that correspond to the vouch IDs mentioned on the payment app within a 12-hour timeframe. Here are the important details to keep in mind:\n\n> Ensure your payment proofs are legitimate\n> The vouch IDs must match those on the payment app\n\n> You have 12 hours to complete this process",
        "To get your vouches, you gotta prove they're yours. So, make sure to show legit payment proofs that match the vouch IDs mentioned on the payment app. You've got 12 hours to do this. Here are the key things to remember:\n\n> Valid payment proofs required\n> Vouch IDs must match those on the payment app\n\n> You have 12 hours to complete it\n\nHope that's clear enough for you!",
        "To claim your vouches, you need to prove they belong to you. Please provide genuine payment proofs that match the vouch IDs mentioned on the payment app within a 12-hour timeframe. Remember these important points:\n\n> Valid payment proofs are necessary\n> Vouch IDs must match the ones on the payment app\n\n> You have 12 hours to complete the process",
        "To access your vouches, you must verify that they are rightfully yours. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Here are some important points to remember:\n\n> Valid payment proofs are required\n> Make sure the vouch IDs match the ones on the payment app\n\n> The deadline for submission is 12 hours",
        "To claim your vouches, it's necessary to demonstrate ownership. Please provide valid payment proofs that correspond to the vouch IDs mentioned on the payment app within the next 12 hours. Remember the following key points:\n\n> Valid payment proofs are necessary\n> Ensure the vouch IDs match those on the payment app\n\n> You have a 12-hour deadline to complete this task",
        "To receive your vouches, you need to prove that they belong to you. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Here are the key points to remember:\n\n> Make sure your payment proofs are valid.\n> The vouch IDs must match those on the payment app.\n\n> You have 12 hours to complete this process.",
        "In order to claim your vouches, it's essential to provide evidence confirming your ownership. Please submit valid payment proofs that correspond to the vouch IDs mentioned on the payment app within a 12-hour timeframe. Remember these important details:\n\n> Valid payment proofs are required.\n> Ensure that the vouch IDs match those on the payment app.\n\n> You have 12 hours to complete this task.",
        "To access your vouches, you must verify that they are rightfully yours. Kindly provide valid payment proofs that align with the vouch IDs specified on the payment app within the next 12 hours. Keep in mind the following key points:\n\n> Valid payment proofs are necessary.\n> The vouch IDs must match those on the payment app.\n\n> You have 12 hours to complete this process.",
        "To claim your vouches, you need to demonstrate ownership. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Remember these important points:\n\n> Valid payment proofs are required.\n> Make sure the vouch IDs match the ones on the payment app.\n\n> You have 12 hours to complete this.",
        "To validate your vouches, you must provide proof of ownership. Please submit valid payment proofs that correspond to the vouch IDs mentioned on the payment app within the next 12 hours. Keep these key points in mind:\n\n> Valid payment proofs are required.\n> Ensure that the vouch IDs match those on the payment app.\n\n> You have a 12-hour deadline to complete this task.",
        "To claim your vouches, it's important to prove that they belong to you. Please ensure you provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Consider the following key points:\n\n> Valid payment proofs are required.\n> The vouch IDs must match those on the payment app.\n\n> You have a 12-hour deadline to complete this.",
        "To access your vouches, you need to verify that they are rightfully yours. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Consider the following key points:\n\n> Valid payment proofs are required.\n> The vouch IDs should align with those on the payment app.\n\n> You have a 12-hour deadline to complete this task.",
        "To claim your vouches, it's necessary to demonstrate that they belong to you. Please ensure you provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Remember the following key points:\n\n> Valid payment proofs are required.\n> The vouch IDs should match those on the payment app.\n\n> You have a 12-hour timeframe to complete this process.",
        "To validate your vouches, you must provide proof of ownership. Please submit valid payment proofs that correspond to the vouch IDs mentioned on the payment app within the next 12 hours. Keep these key points in mind:\n\n> Valid payment proofs are required.\n> Ensure that the vouch IDs match those on the payment app.\n\n> You have a 12-hour deadline to complete this task.",
        "To claim your vouches successfully, it's crucial to provide evidence that proves your ownership. Please submit valid payment proofs that align with the vouch IDs specified on the payment app within the next 12 hours. Remember these important details:\n\n> Valid payment proofs are necessary.\n> The vouch IDs must match those on the payment app.\n\n> You have a 12-hour timeframe to complete this process.",
        "In order to access your vouches, you need to verify that they are rightfully yours. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Consider the following key points:\n\n> Valid payment proofs are required.\n> Make sure the vouch IDs align with those on the payment app.\n\n> You have a 12-hour deadline to complete this task.",
        "To claim your vouches, it's important to prove your ownership. Please ensure you provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Remember these important points:\n\n> Valid payment proofs are necessary.\n> The vouch IDs must align with those on the payment app.\n\n> You have a 12-hour deadline to complete this.",
        "To access your vouches, you must verify that they are indeed yours. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Consider the following key points:\n\n> Valid payment proofs are required.\n> Make sure the vouch IDs match the ones on the payment app.\n\n> You have 12 hours to complete it",
        "To claim your vouches, you need to prove that they're yours. So, make sure to show legit payment proofs that match the vouch IDs mentioned on the payment app. You've got 12 hours to do this. Here are the key things to remember:\n\n> Valid payment proofs required\n> Vouch IDs must match those on the payment app\n\n> You have 12 hours to complete it\n\nHope that's clear enough for you!",
        "To receive your vouches, you need to prove that they belong to you. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Here are the key points to remember:\n\n> Valid payment proofs are necessary.\n> The vouch IDs must match those on the payment app.\n\n> You have 12 hours to complete this process.",
        "To claim your vouches, you must prove that they're yours. So, make sure to provide legit payment proofs that match the vouch IDs mentioned on the payment app. You got 12 hours to do this. Important points:\n\n> Valid payment proofs required\n> Vouch IDs must match those on the payment app\n\n> 12-hour deadline\n\nHope that's clear enough!",
        "To claim your vouches, you need to prove that they are indeed yours. Please submit valid payment proofs that align with the vouch IDs specified on the payment app within the next 12 hours. Keep in mind the following key points:\n\n> Valid payment proofs are necessary.\n> The vouch IDs must match those on the payment app.\n\n> You have 12 hours to complete this task",
        "To validate and redeem your vouches, it's necessary to verify their ownership. Kindly submit authentic payment evidence that corresponds to the vouch IDs specified on the payment application within a 12-hour timeframe. Take note of the following important points:\n\n> Please provide valid payment proofs\n> Ensure that the vouch IDs match those on the payment app\n\n> The deadline for submission is 12 hours",
        "To claim your vouches, you need to prove that they belong to you. Please provide genuine payment proofs that match the vouch IDs mentioned on the payment app within a 12-hour timeframe. Here are the important details to keep in mind:\n\n> Ensure your payment proofs are legitimate\n> The vouch IDs must match those on the payment app\n\n> You have 12 hours to complete this process",
        "To get your vouches, you gotta prove they're yours. So, make sure to provide legit payment proofs that match the vouch IDs mentioned on the payment app. You've got 12 hours to do this. Here are the key things to remember:\n\n> Valid payment proofs required\n> Vouch IDs must match those on the payment app\n\n> You have 12 hours to complete it\n\nHope that's clear enough for you!",
        "To claim your vouches, it's necessary to demonstrate ownership. Please provide valid payment proofs that correspond to the vouch IDs mentioned on the payment app within the next 12 hours. Remember the following key points:\n\n> Valid payment proofs are necessary\n> Ensure the vouch IDs match those on the payment app\n\n> You have a 12-hour deadline to complete this task",
        "To access your vouches, you must verify that they are rightfully yours. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Here are some important points to remember:\n\n> Valid payment proofs are required\n> Make sure the vouch IDs match the ones on the payment app\n\n> The deadline for submission is 12 hours",
        "To claim your vouches, it's necessary to prove that they belong to you. Please provide valid payment proofs that correspond to the vouch IDs mentioned on the payment app within the next 12 hours. Remember the following key points:\n\n> Valid payment proofs are necessary\n> Ensure the vouch IDs match those on the payment app\n\n> You have a 12-hour deadline to complete this task",
        "To receive your vouches, you need to prove that they belong to you. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Here are the key points to remember:\n\n> Valid payment proofs are necessary\n> The vouch IDs must match those on the payment app\n\n> You have 12 hours to complete this process",
        "To claim your vouches, it's important to prove that they're yours. Please make sure to provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Consider the following key points:\n\n> Valid payment proofs are required\n> The vouch IDs must match those on the payment app\n\n> You have a 12-hour deadline to complete this task",
        "To access your vouches, you need to verify that they are indeed yours. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Remember these key points:\n\n> Valid payment proofs are required\n> The vouch IDs must match those on the payment app\n\n> You have 12 hours to complete this process",
        "To claim your vouches, you must prove that they are yours. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Here are the important details to remember:\n\n> Valid payment proofs required\n> Vouch IDs must match those on the payment app\n\n> 12-hour deadline\n\nHope that's clear enough!",
        "To claim your vouches, it's important to verify their ownership. Please provide valid payment proofs that align with the vouch IDs specified on the payment app within the next 12 hours. Keep in mind the following key points:\n\n> Valid payment proofs are necessary\n> The vouch IDs must match those on the payment app\n\n> You have 12 hours to complete this task",
        "To validate and redeem your vouches, it's necessary to verify their ownership. Kindly submit authentic payment evidence that corresponds to the vouch IDs specified on the payment application within a 12-hour timeframe. Take note of the following important points:\n\n> Please provide valid payment proofs\n> Ensure that the vouch IDs match those on the payment app\n\n> The deadline for submission is 12 hours",
        "To claim your vouches, you need to prove that they belong to you. Please provide genuine payment proofs that match the vouch IDs mentioned on the payment app within a 12-hour timeframe. Here are the important details to keep in mind:\n\n> Ensure your payment proofs are legitimate\n> The vouch IDs must match those on the payment app\n\n> You have 12 hours to complete this process",
        "To get your vouches, you need to prove that they're yours. So, make sure to provide valid payment proofs that match the vouch IDs mentioned on the payment app. You have 12 hours to do this. Here are the key points to remember:\n\n> Valid payment proofs required\n> Vouch IDs must match those on the payment app\n\n> You have 12 hours to complete it\n\nHope that's clear enough!",
        "To claim your vouches, it's necessary to demonstrate ownership. Please provide valid payment proofs that correspond to the vouch IDs mentioned on the payment app within the next 12 hours. Remember the following key points:\n\n> Valid payment proofs are necessary\n> Ensure the vouch IDs match those on the payment app\n\n> You have a 12-hour deadline to complete this task",
        "To access your vouches, you must verify that they are rightfully yours. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Here are some important points to remember:\n\n> Valid payment proofs are required\n> Make sure the vouch IDs match the ones on the payment app\n\n> The deadline for submission is 12 hours",
        "To claim your vouches, it's necessary to prove that they belong to you. Please provide valid payment proofs that correspond to the vouch IDs mentioned on the payment app within the next 12 hours. Remember the following key points:\n\n> Valid payment proofs are necessary\n> Ensure the vouch IDs match those on the payment app\n\n> You have a 12-hour deadline to complete this task",
        "To receive your vouches, you need to prove that they belong to you. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Here are the key points to remember:\n\n> Valid payment proofs are necessary\n> The vouch IDs must match those on the payment app\n\n> You have 12 hours to complete this process",
        "To claim your vouches, it's important to prove that they're yours. Please make sure to provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Consider the following key points:\n\n> Valid payment proofs are required\n> The vouch IDs must match those on the payment app\n\n> You have a 12-hour deadline to complete this task",
        "To access your vouches, you need to verify that they are indeed yours. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Remember these key points:\n\n> Valid payment proofs are required\n> The vouch IDs must match those on the payment app\n\n> You have 12 hours to complete this process",
        "To claim your vouches, you must prove that they are yours. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Here are the important details to remember:\n\n> Valid payment proofs required\n> Vouch IDs must match those on the payment app\n\n> 12-hour deadline\n\nHope that's clear enough!",
        "To claim your vouches, it's important to verify their ownership. Please provide valid payment proofs that align with the vouch IDs specified on the payment app within the next 12 hours. Keep in mind the following key points:\n\n> Valid payment proofs are necessary\n> The vouch IDs must match those on the payment app\n\n> You have 12 hours to complete this task",
        "To validate and redeem your vouches, it's necessary to prove their ownership. Kindly submit authentic payment evidence that corresponds to the vouch IDs specified on the payment application within a 12-hour timeframe. Take note of the following important points:\n\n> Please provide valid payment proofs\n> Ensure that the vouch IDs match those on the payment app\n\n> The deadline for submission is 12 hours",
        "To claim your vouches, you need to prove that they belong to you. Please provide genuine payment proofs that match the vouch IDs mentioned on the payment app within a 12-hour timeframe. Here are the important details to keep in mind:\n\n> Ensure your payment proofs are legitimate\n> The vouch IDs must match those on the payment app\n\n> You have 12 hours to complete this process",
        "To get your vouches, you need to prove that they're yours. So, make sure to provide valid payment proofs that match the vouch IDs mentioned on the payment app. You have 12 hours to do this. Here are the key points to remember:\n\n> Valid payment proofs required\n> Vouch IDs must match those on the payment app\n\n> You have 12 hours to complete it\n\nHope that's clear enough!",
        "To claim your vouches, it's necessary to demonstrate ownership. Please provide valid payment proofs that correspond to the vouch IDs mentioned on the payment app within the next 12 hours. Remember the following key points:\n\n> Valid payment proofs are necessary\n> Ensure the vouch IDs match those on the payment app\n\n> You have a 12-hour deadline to complete this task",
        "To access your vouches, you must verify that they are rightfully yours. Please provide valid payment proofs that match the vouch IDs mentioned on the payment app within the next 12 hours. Here are some important points to remember:\n\n> Valid payment proofs are required\n> Make sure the vouch IDs match the ones on the payment app\n\n> The deadline for submission is 12 hours",
        "To claim your vouches, it's necessary to prove that they belong to you. Please provide valid payment proofs that correspond to the vouch IDs mentioned on the payment app within the next 12 hours. Remember the following key points:\n\n> Valid payment proofs are necessary\n> Ensure the vouch IDs match those on the payment app\n\n> You have a 12-hour deadline to complete this task",
    ]
    message = random.choice(messages)
    await ctx.send(message)







#----------------------------------Swift Commands to be deleted
@bot.command()
async def a(ctx):
    await ctx.message.delete()

@bot.command()
async def p(ctx):
    await ctx.message.delete()

@bot.command()
async def pending(ctx):
    await ctx.message.delete()

@bot.command()
async def d(ctx):
    await ctx.message.delete()

@bot.command()
async def view_denied(ctx):
    await ctx.message.delete()

@bot.command()
async def proof(ctx):
    await ctx.message.delete()

@bot.command()
async def view_pending(ctx):
    await ctx.message.delete()

@bot.command()
async def get(ctx):
    await ctx.message.delete()

@bot.command()
async def flag(ctx):
    await ctx.message.delete()

@bot.command()
async def view(ctx):
    await ctx.message.delete()

@bot.command()
async def staffnote(ctx):
    await ctx.message.delete()

@bot.command()
async def approve(ctx):
    await ctx.message.delete()

@bot.command()
async def deny(ctx):
    await ctx.message.delete()

#-------------------------Staffping Warning(Verbal)


@bot.command()
async def staffping(ctx, channel: discord.TextChannel = None):
    await ctx.message.delete()  # Delete the trigger message

    message = "__**Please Avoid Pinging Staff**__\n\nAvoid pinging or mentioning staff unnecessarily to get a faster response to your ticket. Be patient and follow up politely if needed. Also, avoid reply mentions when responding to staff messages to prevent further delays.\n\nGIF for reference: https://tenor.com/view/mention-stop-dont-ping-ping-discord-gif-19964821"

    if channel is not None:
        await channel.send(message)  # Send the message to the specified channel
    else:
        await ctx.send(message)  # Send the message to the channel where the trigger was used


#------------------------Mention Vouch IDs

@bot.command()
async def mentionvouch(ctx):
        await ctx.message.delete()
        message = f" __**Mention the Vouch IDs Correctly**__ in order to get the reference of all the proofs , otherwise ticket won't be entertained."
        await ctx.send(message)  





#------------------------Vouch Deletion Message in swift Chat (Requesting Swift Admin)

@bot.command()
async def vouchdelete(ctx, *, message):
    channel = bot.get_channel(892443143566405653)
    await ctx.message.delete()
    try:
        await channel.send(f"Please delete {message} these vouches <@1073087362097229824>")
        await ctx.send("Deletion message sent sucessfully successfully!", delete_after=3)
    except:
        await ctx.send("Failed to send vouch deletion message", delete_after=5)
        await ctx.message.delete()

      
    



  
      
#------------------------Vouch import message

@bot.command()
async def vouchimport(ctx, *, message):
    await ctx.message.delete()
    response = f"{message}\n\n> Payment proof ✅\n\n> <@&888763368943534101>"
    await ctx.send(response)


#----------------How The payment proof should look like Tutorial

@bot.command(name='proofinfo')
async def proofinfo(ctx):
    await ctx.message.delete()
    response = """When submitting proofs, it's important to follow certain guidelines to ensure that they are valid and can be processed efficiently. To ensure that your proofs are acceptable, please keep in mind the following:

> ・Proofs must be submitted without any cropping or editing.
> 
> ・Screenshots must be taken from the payment app and should be up-to-date to ensure validity.
> 
> ・If you're using a Windows or Mac computer, please include your window dock and browser dock in the screenshot."""
    await ctx.send(response)



#------------------------12-Hour Wait for Verification
@bot.command()
async def vouch12hr(ctx):
    vouch12hrmessages = [
    "Thank you for submitting your proofs! We will review them within the next 12 hours. Once they have been approved, **our administrators will be notified to proceed with importing your vouch profile**.",
    "Thank you for sending in your proofs! Our team will carefully review them in the next 12 hours. After they have been verified, **our administrators will be notified to import your vouch profile**.",
    "We appreciate you submitting your proofs! Our team will diligently assess them in the next 12 hours. Once they are validated, **our administrators will be notified to handle the import of your vouch profile**.",
    "Thank you for sharing your proofs! Our team will conduct a thorough review within the next 12 hours. Upon approval, **our administrators will be notified to import your vouch profile as requested**.",
    "We have received your proofs. Our team will review them within the next 12 hours. Once they have been approved, **our administrators will be notified to import your vouch profile**.",
    "Thank you for providing your proofs! We will carefully review them in the next 12 hours. After approval, **our administrators will be notified to handle the import process for your vouch profile**.",
    "We acknowledge the receipt of your proofs. Our team will review them within the next 12 hours. **Upon approval, our administrators will be notified to proceed with importing your vouch profile**.",
    "Thank you for submitting your proofs! Our team will evaluate them within the next 12 hours. Once approved, **our administrators will be notified to import your vouch profile**.",
    "We have received the proofs you submitted. Our team will review them within the next 12 hours. After they have been approved, **our administrators will be notified to import your vouch profile**.",
    "Thank you for sharing your proofs! Our team will carefully review them within the next 12 hours. Once they are approved, **our administrators will be notified to proceed with importing your vouch profile as requested**.",
    "We appreciate you submitting your proofs! Our team will diligently assess them in the next 12 hours. Upon verification, **our administrators will be notified to handle the import of your vouch profile**.",
    "Thank you for providing your proofs! Our team will conduct a thorough review within the next 12 hours. After validation, **our administrators will be notified to proceed with importing your vouch profile**.",
    "We have received your proofs. Our team will review them within the next 12 hours. Once approved, **our administrators will be notified to import your vouch profile as requested**.",
    "Thank you for sharing your proofs! We will carefully review them in the next 12 hours. After approval, **our administrators will be notified to handle the import process for your vouch profile**.",
    "We acknowledge the receipt of your proofs. Our team will review them within the next 12 hours. **Upon approval, our administrators will be notified to proceed with importing your vouch profile**.",
    "Thank you for submitting your proofs! Our team will evaluate them within the next 12 hours. Once approved, **our administrators will be notified to import your vouch profile accordingly**.",
    "We have received the proofs you submitted. Our team will review them within the next 12 hours. After they have been approved, **our administrators will be notified to import your vouch profile**.",
    "Thank you for sharing your proofs! Our team will carefully review them within the next 12 hours. Once they are approved, **our administrators will be notified to proceed with importing your vouch profile as requested**.",
    "We appreciate you submitting your proofs! Our team will diligently assess them in the next 12 hours. Upon verification, **our administrators will be notified to handle the import of your vouch profile**.",
    "Thank you for providing your proofs! Our team will conduct a thorough review within the next 12 hours. After validation, **our administrators will be notified to proceed with importing your vouch profile**.",
    "We have received your proofs. Our team will review them within the next 12 hours. Once approved, **our administrators will be notified to import your vouch profile as requested**.",
    "Thank you for sharing your proofs! We will carefully review them in the next 12 hours. After approval, **our administrators will be notified to handle the import process for your vouch profile**.",
    "We acknowledge the receipt of your proofs. Our team will review them within the next 12 hours. **Upon approval, our administrators will be notified to proceed with importing your vouch profile**.",
    "Thank you for submitting your proofs! Our team will evaluate them within the next 12 hours. Once approved, **our administrators will be notified to import your vouch profile**.",
    "We have received the proofs you submitted. Our team will review them within the next 12 hours. After they have been approved, **our administrators will be notified to import your vouch profile**.",
    "Thank you for sharing your proofs! Our team will carefully review them within the next 12 hours. Once they are approved, **our administrators will be notified to proceed with importing your vouch profile as requested**.",
    "We appreciate you submitting your proofs! Our team will diligently assess them in the next 12 hours. Upon verification, **our administrators will be notified to handle the import of your vouch profile**.",
    "Thank you for providing your proofs! Our team will conduct a thorough review within the next 12 hours. After validation, **our administrators will be notified to proceed with importing your vouch profile**.",
    "We have received your proofs. Our team will review them within the next 12 hours. Once approved, **our administrators will be notified to import your vouch profile as requested**.",
    "Thank you for sharing your proofs! We will carefully review them in the next 12 hours. After approval, **our administrators will be notified to handle the import process for your vouch profile**.",
    "We acknowledge the receipt of your proofs. Our team will review them within the next 12 hours. **Upon approval, our administrators will be notified to proceed with importing your vouch profile**."
  ]

    
    message = random.choice(vouch12hrmessages)
    await ctx.send(message)
    await ctx.message.delete()

#-------





  
#---------------------vouch_recovery_ticket_starting

@bot.command()
async def vouchrecovery(ctx, user_id):
    await ctx.message.delete()  # delete the trigger message

    # Respond with two messages
    await ctx.send(f" =add {user_id} ")
    await ctx.send(f"+vouches {user_id}")
    await ctx.send(f"<@{user_id}>")

#------------------------Vouch_recovery_dm 

#This_Can_make_your_account_terminated


@bot.command()
async def recoverydm(ctx, user: discord.User):
    # Send direct message to user
    try:
        await ctx.message.delete()  # delete the trigger message
        channel = await user.create_dm()
        await channel.send(f"A request has been submitted by a new account, which may be you, for a vouch import. Please take a look at the import ticket {ctx.channel.mention} and respond within 12hrs if it wasn't initiated by you.\n\n~Scammeralert Team\nhttps://discord.gg/scammeralert")
        await ctx.send(f"Sent recovery DM to {user.mention}.", delete_after=5)
        await ctx.send(f"=rename {ctx.channel.name}-12h")
    except Exception as e:
        error_message = await ctx.send(f"Failed to send recovery DM to {user.mention}: {e}")
        await asyncio.sleep(5)
        await error_message.delete()




#-----------------------How to prove a vouch INfo 
@bot.command()
async def vouchinfo(ctx):
    await ctx.message.delete()
    await ctx.send('**How to Provide Proof of a Vouch**\n\n> To prove a vouch, it is essential to correctly mention the vouch IDs to obtain a reference for verification. Vouch IDs refer to the title of the embedded message for each vouch that was sent. You can either reply to the vouch message or mention the vouch IDs in your response.\n> \n> It is crucial to attach recent and easily accessible proof of the transaction, along with all relevant details. Ensure that the entire transaction details are visible and the window/Mac dock/phone notification (status) bar as well as the navigation bar/browser dock are also visible in the proof. This will make it easier to validate the authenticity of the vouch.')

      
#-----------------------Reminder For a Channel Check within 12hour (Using Either Carl, Flantic or any bot which has ? as prefix and uses ?rm as trigger for taking the command for reminder)
      
  
@bot.command()
async def remindchannel(ctx):
  
    await ctx.send(f'?rm  {ctx.channel.mention} `{ctx.channel}` 12hr')
    await ctx.message.delete()  # Delete the command trigger message



#--------------------------------Vouch For MM , Exch & Selling

#MM
@bot.command()
async def vouchmm(ctx, *, message):
    await ctx.send(f'`+rep {ctx.author.mention} MM | {message}`')
    await ctx.message.delete()

#Selling
@bot.command()
async def vouchsold(ctx, *, message):
    invite_link = "https://discord.gg/BdkryGCQgs"
    await ctx.send(f'`+rep {ctx.author.mention} Sold | {message}`')
    await ctx.send(invite_link)
    await ctx.message.delete()
  
#Exch
@bot.command()
async def vouchexch(ctx, *, message):
    await ctx.send(f'`+rep {ctx.author.mention} Exchange | {message}`')
    await ctx.message.delete()
  
#----------------------------------------Transaction Details (Crypto)

  
@bot.command()
async def check(ctx, arg, args):
    url = f'https://api.blockcypher.com/v1/{arg}/main/txs/{args}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        confirmations = data['confirmations']
        preference = data['preference']
        confirmed = data.get('confirmed', 'Not confirmed').replace('T', ' ').replace('Z', '')
        received = data.get('received', 'Not received').replace('T', ' ').replace('Z', '')
        double_spend = data['double_spend']

        # Extract receiver and sender addresses
        for output in data['outputs']:
            if 'addresses' in output.keys():
                if output['addresses'][0] != data['inputs'][0]['addresses'][0]:
                    receiver_address = output['addresses'][0]
                    sender_address = data['inputs'][0]['addresses'][0]
                    break
        
        # Get price of transaction
        output_values = [output['value'] for output in data['outputs']]
        price = sum(output_values) / 10 ** 8 # divide by 10^8 to convert from satoshis to the base unit of the cryptocurrency
        
        # Format the confirmed and received timestamps using Discord's timestamp format
        confirmed_timestamp = int(datetime.fromisoformat(confirmed).timestamp())
        confirmed_formatted = f"<t:{confirmed_timestamp}:F>"
        received_timestamp = int(datetime.fromisoformat(received).timestamp())
        received_formatted = f"<t:{received_timestamp}:F>"
        
        await ctx.reply(f'Sender Address: {sender_address}\nReceiver Address: {receiver_address}\nConfirmations: {confirmations}\nPreference: {preference}\nConfirmed: {confirmed_formatted}\nReceived: {received_formatted}\nDouble Spend: {double_spend}\nCrypto Transacted: {price} {arg.upper()}')
    else:
        await ctx.reply('Invalid Transaction ID')
    
  
#-------------------------------Basic Maths Calculation (Such as +,-,* or /)

      
@bot.command()
async def calc(ctx, *, expression):
    try:
        result = eval(expression)
        await ctx.message.delete()
        await ctx.send(f"{expression} = {result}")
    except:
        await ctx.send('Invalid expression')




#------------------------------Universal Bot Commands

#1
@bot.command()
async def mplay(ctx, *, message):
    channel = bot.get_channel(1083636551092797510)
    await channel.send(f'+play {message}')
    await ctx.message.delete()  # Deletes the message sent by the user

@bot.command()
async def mvc(ctx):
    await ctx.send('<#1083637097254096936>')
    await ctx.message.delete()     

@bot.command()
async def mskip(ctx):
    channel = bot.get_channel(1083636551092797510)
    await channel.send('+skip')
    await ctx.message.delete()

@bot.command()
async def mvolume(ctx, message):
    channel = bot.get_channel(1083636551092797510)
    await channel.send(f'+volume {message}')
    await ctx.message.delete()

#2



@bot.command()
async def hplay(ctx, *, message):
    channel = bot.get_channel(985557881749393458)
    await channel.send(f'+play {message}')
    await ctx.message.delete()  # Deletes the message sent by the user

@bot.command()
async def hvc(ctx):
    await ctx.send('<#981267051513520148>')
    await ctx.message.delete()     

@bot.command()
async def hskip(ctx):
    channel = bot.get_channel(985557881749393458)
    await channel.send('+skip')
    await ctx.message.delete()

@bot.command()
async def hvolume(ctx, message):
    channel = bot.get_channel(985557881749393458)
    await channel.send(f'+volume {message}')
    await ctx.message.delete()  


#--------------------------Token Info Command
#under Build


#------------------------------------------Friends relation commands


@bot.command()  
async def unfriend(ctx, *, user: discord.User):
    await user.remove_friend()
    await ctx.send(f"{user.mention} has been unfriended!", delete_after=3)
    await ctx.message.delete()



#-------------------------Userinfo
@bot.command()
async def userinfo(ctx, user: discord.User):
    # Get the user's information
    username = user.name
    discriminator = user.discriminator
    user_tag = f"{username}#{discriminator}"
    user_id = user.id
    created_at = user.created_at
    account_age = (datetime.now() - created_at).days
    avatar_url = user.avatar_url

    # Convert the creation time to Unix timestamp format
    created_at_timestamp = int(created_at.timestamp())
    created_at_str = str(created_at_timestamp)

    # Format the account creation time using Discord's timestamp format
    created_at_formatted = f"<t:{created_at_str}:F>"

    # Create the response message
    response = (f"> **User Name**: `{username}`\n"
                f"> **User Tag**: `{user_tag}`\n"
                f"> **User ID**: `{user_id}`\n"
                f"> **Account Age**: `{account_age} days` (Created on {created_at_formatted})\n"
                f"> **Avatar URL**: `{avatar_url}`")

    # Send the message to the channel
    await ctx.send(response)

    # Delete the user's trigger message
    await ctx.message.delete()

  #-------------------snipe

# Dictionaries to store deleted and edited messages
snipe_message_author = {}
snipe_message_content = {}
snipe_message_created = {}

esnipe_message_author = {}
esnipe_message_created = {}
esnipe_message_before = {}
esnipe_message_after = {}

# Event handler for message delete
@bot.event
async def on_message_delete(message):
    if message.content == f"{prefix}snipe":  # Ignore snipe command messages
        return
    else:
        snipe_message_author[message.channel.id] = message.author
        snipe_message_content[message.channel.id] = message.content
        snipe_message_created[message.channel.id] = message.created_at

# Event handler for message edit
@bot.event
async def on_message_edit(before, after):
    esnipe_message_author[before.channel.id] = before.author
    esnipe_message_created[before.channel.id] = before.created_at
    esnipe_message_before[before.channel.id] = before.content
    esnipe_message_after[before.channel.id] = after.content

# Command to retrieve sniped messages
@bot.command()
async def snipe(ctx):
    try:
        await ctx.message.delete()
        channel = ctx.channel
        try:
            await ctx.send(f"─────────────────────\n**Message Deleted**\n\n> **Message content -** `{snipe_message_content[channel.id]}`\n> **Message sent by -** `{snipe_message_author[channel.id]}`\n> **Message created at -** `{snipe_message_created[channel.id]}`\n─────────────────────")
        except:
            await ctx.send(f"`There are no recently deleted messages in {channel.name}`")
            pass
        try:
            await ctx.send(f"─────────────────────\n**Message Edited**\n\n> **Before -** `{esnipe_message_before[channel.id]}`\n> **After -** `{esnipe_message_after[channel.id]}`\n> **Message sent by -** `{esnipe_message_author[channel.id]}`\n> **Message created at -** `{esnipe_message_created[channel.id]}`\n─────────────────────")
        except:
            await ctx.send(f"`There are no recently edited messages in {channel.name}`")
            pass

    except KeyError:
        await ctx.send(f"`There are no recently deleted or edited messages in {channel.name}`")

# Function to clear sniped messages from the dictionaries
async def clear_snipe_messages():
    snipe_message_author.clear()
    snipe_message_content.clear()
    snipe_message_created.clear()
    esnipe_message_author.clear()
    esnipe_message_created.clear()
    esnipe_message_before.clear()
    esnipe_message_after.clear()

# Scheduled task to clear sniped messages every 1 minutes
async def schedule_clear_snipe_messages():
    while True:
        await asyncio.sleep(60)  # Sleep for 1 minutes (6 * 60 seconds)
        await clear_snipe_messages()

# Start the bot and schedule the task as a background task
bot.loop.create_task(schedule_clear_snipe_messages())







#-------------nickname command which works somehow

@bot.command()
async def nick(ctx, member: discord.Member = None, *, nickname=None):
    if not member:
        # Check if the first argument is a member mention
        if ctx.message.mentions:
            member = ctx.message.mentions[0]
        # Otherwise, check if the first argument is a user ID
        else:
            try:
                member_id = int(ctx.message.content.split()[1])
                member = await ctx.guild.fetch_member(member_id)
            except (ValueError, IndexError, discord.NotFound):
                member = ctx.author
    if not nickname:
        await ctx.send("Please provide a new nickname.")
        return
    try:
        await member.edit(nick=nickname)
        msg = await ctx.send(f"Nickname changed to {nickname} for {member.display_name}.")
        await asyncio.sleep(3)  # wait for 3 seconds
        await ctx.message.delete()  # delete the command message
        await msg.delete()  # delete the response message
    except discord.Forbidden:
        await ctx.send("I do not have the permissions to change that user's nickname.")




#----scrape text channel 


@bot.command()
async def scrapetxtchannels(ctx):
    text_channels = ctx.guild.text_channels
    channel_ids = [channel.id for channel in text_channels]
    channel_ids_str = "\n".join(map(str, channel_ids))

    with open("channel_ids.txt", "w") as f:
        f.write(channel_ids_str)

    await ctx.send("The channel ids scraped are:", file=discord.File("channel_ids.txt"))



  #-----------------purge test 

@bot.command()
async def purge(ctx, amount=10):
    await ctx.message.delete()
    channel = ctx.channel
    author = ctx.author
    messages = []
    async for message in channel.history(limit=amount):
        if message.author == author:
            messages.append(message)

    if len(messages) == 0:
        await ctx.send(f"**No messages found to purge for {author.mention}** !", delete_after=3)
        return

    for message in messages:
        await message.delete()
        await asyncio.sleep(1)

    await ctx.send(f"> **Deleted `{len(messages)}` messages for {author.mention} !**", delete_after=3)

  
#-----------------------------Ping 
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"> **Ping** : `{latency}ms`", delete_after=3)
    await ctx.message.delete()

#----------------------post after a interval 

@bot.command()
async def post(ctx, channel: discord.TextChannel, interval: int, *, message):
    while True:
        await channel.send(message)
        await asyncio.sleep(interval)
#---------------------post in that channel every random interval
@bot.command()
async def randompost(ctx, channel: discord.TextChannel, min_interval: int, max_interval: int, *, message):
    while True:
        interval = random.randint(min_interval, max_interval)
        await channel.send(message)
        await asyncio.sleep(interval)

#-------------------Post Ads
@bot.command()
async def postad(ctx, channel: discord.TextChannel, interval: int, *, message):
    await ctx.message.delete()
    last_message = None  # Keep track of the last sent message

    while True:
        if last_message:
            try:
                await last_message.delete()
            except discord.errors.NotFound:
                # If the last message was deleted, set last_message to None
                last_message = None

        # Send a new message and update the last sent message
        last_message = await channel.send(message)

        await asyncio.sleep(interval)
#----------------------Server Leave 
@bot.command()
async def leave(ctx, server_id: int = None):
    if server_id:
        guild = bot.get_guild(server_id)
        if guild is None:
            await ctx.send('Invalid server ID. Please specify a valid server ID.')
            return
    else:
        guild = ctx.guild

    if ctx.author.id == guild.owner_id:
        await ctx.send('You cannot leave this guild!')
    else:
        leave_delay = 1.0 # seconds
        await asyncio.sleep(leave_delay)
        await guild.leave()
        print(f'Left server {guild.name}!')

#---------------------Crypto Address Info
@bot.command()
async def cryptoaddress(ctx, coin, address):
    # Fetch information for the given cryptocurrency address
    try:
        # Get the cryptocurrency address details using BlockCypher API
        address_details = get_address_full(address=address, coin_symbol=coin)

        # Extract relevant information from the response
        balance = address_details['final_balance'] / 10**8  # Convert satoshis to BTC for Bitcoin, or equivalent for other coins
        total_received = address_details['total_received'] / 10**8
        total_sent = address_details['total_sent'] / 10**8
        transaction_count = address_details['n_tx']
        last_transactions = address_details['txs'][:5]  # Get the last 5 transactions

        # Format the response message
        response = f"**Cryptocurrency Address Details**\n\n" \
                   f"> Coin: {coin}\n" \
                   f"> Address: {address}\n" \
                   f"> Balance: {balance} {coin}\n" \
                   f"> Total Received: {total_received} {coin}\n" \
                   f"> Total Sent: {total_sent} {coin}\n" \
                   f"> Transaction Count: {transaction_count}\n\n"

        # Add last 5 transaction details to the response message
        response += f"**Last 5 Transactions:**\n"
        for transaction in last_transactions:
            transaction_hash = transaction['hash']
            transaction_confirmations = transaction['confirmations']
            transaction_link = f"https://live.blockcypher.com/{coin}/tx/{transaction_hash}"  # Replace with appropriate link for the cryptocurrency
            response += f"----------------------------------------\n" \
                        f"Transaction Hash: {transaction_hash}\n" \
                        f"Transaction Link: {transaction_link}\n" \
                        f"Confirmations: {transaction_confirmations}\n" \
                        f"----------------------------------------"

        # Send the response message
        await ctx.send(response)

    except Exception as e:
        # Handle any errors that may occur
        await ctx.send(f"Error: {e}")

#-------------------SS{screenshot of a url} 

@bot.command(name="screenshot", aliases=["ss"])
async def screenshot(ctx, url):
    await ctx.message.delete()  # add this line to delete the trigger message
    user = ctx.author.name
    if not url:
      await ctx.send(f"{user}, where is the link?", delete_after=5)
      return
    
    if len(url) < 8:
      await ctx.reply("https is too short to reach - 8 limit", delete_after=9)
      return

    async with ctx.typing():
        site = url if url.startswith('http') else f'http://{url}'
        try:
            response = requests.get(f'https://image.thum.io/get/width/1920/crop/675/noanimate/{site}')
            file = io.BytesIO(response.content)
            await ctx.send(f"Here is a screenshot from requested URL:", file=discord.File(file, filename="Screenshot.png"))
        except requests.exceptions.InvalidURL:
            await ctx.send("Invalid URL", delete_after=9)
        except:
            await ctx.send(f"Error Occured", delete_after=9)



#-------------Gsearch/Google Search



#----Gsearch
@bot.command()
async def gsearch(ctx, *, query):
    query = urllib.parse.quote(query)  # URL encode the query
    search_url = f'https://www.google.com/search?q={query}'
    
    async with ctx.typing():
        await ctx.send(f"Google search results for '{query}':")
        await ctx.send(search_url)

        try:
            response = requests.get(f'https://image.thum.io/get/width/1920/crop/675/noanimate/{search_url}')
            file = io.BytesIO(response.content)
            await ctx.send("Here is a screenshot of the Google search results:", file=discord.File(file, filename="Search_Screenshot.png"))
        except:
            await ctx.send("An error occurred while capturing the screenshot.")



#---------------Restart 

@bot.command()
async def restart(ctx):
    await ctx.reply('Restarting...')
    os.execl(sys.executable, sys.executable, *sys.argv)
  #------------End 






try:
    bot.run(token)
