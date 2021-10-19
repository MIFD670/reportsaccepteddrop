import datetime

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class AcceptReport(commands.Cog): 
    """Allows Drop Staff members to accept reports to be added to the ban database"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.api.get_plugin_partition(self)

    @commands.command(aliases=["rchannel"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def reportchannel(self, ctx, channel: discord.TextChannel):
        """Set the accepted reports channel"""
        await self.db.find_one_and_update({"_id": "config"}, {"$set": {"accept_reports_channel": channel.id}}, upsert=True)
        
        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Set Channel", value=f"Successfully set the Accepted Reports channel to {channel.mention}", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command()
    async def report(self, ctx, user: discord.Member, *, ticketlink: str, reason: str, proof: str):
        """Allows Drop Staff members to accept reports"""
        config = await self.db.find_one({"_id": "config"})
        report_channel = config["accept_reports_channel"]
        setchannel = discord.utils.get(ctx.guild.channels, id=int(report_channel))
        
        report_mention = ""
            
        embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        
        embed.setTitle(name="Drop Scam & Fraud - Staff Member Accepted Report")
        embed.add_field(name="Reported user:", value=f"{user.mention} | ID: {user.id}", inline=False)
        embed.add_field(name="Staff member:", value=f"{ctx.author.mention} | ID: {ctx.author.id}", inline=False)
        embed.add_field(name="Ticket Link:", value=f"{ticketlink}", inline=False)
        embed.add_field(name="Ticket:", value=ctx.channel.mention, inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Proof:", value=f"{proof}", inline=False)

        await setchannel.send(report_mention, embed=embed)
        await ctx.send("Succesfully submitted the report to be accepted by a supervisor!")
                        
def setup(bot):
    bot.add_cog(AcceptReport(bot))