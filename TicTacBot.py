import discord
from discord import app_commands

token = open("TicToken.txt", "r") #opens bot auth token
custom_status = "/play"
guild_id = open("TicId.txt", "r") #server id where bot is active

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents) #creates client with desires permissions
tree = app_commands.CommandTree(client)

class Buttons(discord.ui.View): #creates subclass of View() to contain button info
    def __init__(self, *, timeout=180):
        self.currentStyle = discord.ButtonStyle.green
        self.currentSymbol = "X"
        self.board = [["","",""],["","",""],["","",""]]
        super().__init__(timeout=timeout)

    @discord.ui.button(label="-", row=0, style=discord.ButtonStyle.primary, custom_id="00")
    async def top_left_callback(self, interaction, button):
        await self.processPush(interaction, button)

    @discord.ui.button(label="-", row=0, style=discord.ButtonStyle.primary, custom_id="01")
    async def top_mid_callback(self, interaction, button):
        await self.processPush(interaction, button)

    @discord.ui.button(label="-", row=0, style=discord.ButtonStyle.primary, custom_id="02")
    async def top_right_callback(self, interaction, button):
        await self.processPush(interaction, button)

    @discord.ui.button(label="-", row=1, style=discord.ButtonStyle.primary, custom_id="10")
    async def mid_left_callback(self, interaction, button):
        await self.processPush(interaction, button)

    @discord.ui.button(label="-", row=1, style=discord.ButtonStyle.primary, custom_id="11")
    async def mid_callback(self, interaction, button):
        await self.processPush(interaction, button)

    @discord.ui.button(label="-", row=1, style=discord.ButtonStyle.primary, custom_id="12")
    async def mid_right_callback(self, interaction, button):
        await self.processPush(interaction, button)

    @discord.ui.button(label="-", row=2, style=discord.ButtonStyle.primary, custom_id="20")
    async def bot_left_callback(self, interaction, button):
        await self.processPush(interaction, button)

    @discord.ui.button(label="-", row=2, style=discord.ButtonStyle.primary, custom_id="21")
    async def bot_mid_callback(self, interaction, button):
        await self.processPush(interaction, button)

    @discord.ui.button(label="-", row=2, style=discord.ButtonStyle.primary, custom_id="22")
    async def bot_right_callback(self, interaction, button):
        await self.processPush(interaction, button)

    async def processPush(self, interaction, button):
        #takes 1st and 2nd number from custom id to find row and col info
        self.board[int(interaction.data["custom_id"][:1])][int(interaction.data["custom_id"][1:])] = self.currentSymbol
        #updates selected button to have color and symbol of active player
        button.label = self.currentSymbol
        button.style = self.currentStyle

        if (await self.winChecker()):
            for child in self.children:
                child.disabled = True
            await interaction.response.edit_message(content=f"Winner is {self.currentSymbol}", view=self)

        elif (self.currentSymbol == "X"):
            button.disabled = True
            self.currentSymbol = "O"
            self.currentStyle = discord.ButtonStyle.red
            await interaction.response.edit_message(content=f"{self.currentSymbol}'s turn", view=self)

        else:
            button.disabled = True
            self.currentSymbol = "X"
            self.currentStyle = discord.ButtonStyle.green
            await interaction.response.edit_message(content=f"{self.currentSymbol}'s turn", view=self)
    
    async def winChecker(self):
        for row in range(0,3):
            if ((self.board[row][0] == self.board[row][1] == self.board[row][2]) and (self.board[row][0] != "")):
                #print(f"winner is {board[row][0]}")
                return True

        for col in range(0,3):
            if ((self.board[0][col] == self.board[1][col] == self.board[2][col]) and (self.board[0][col] != "")):
                return True

        if ((self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] != "")):
            return True

        if ((self.board[2][0] == self.board[1][1] == self.board[0][2]) and (self.board[2][0] != "")):
            return True
        #print("false" + board[0][0]+board[1][1]+board[2][2])
        return False

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id.read()))
    await client.change_presence(activity=discord.Game(custom_status))
    print("ready")

@tree.command(name= "play", description="Play a game of tic-tac-toe", guild=discord.Object(id=guild_id.read()))
async def game(interaction):
    await interaction.response.send_message("X's turn", ephemeral=True, view=Buttons())

client.run(token.read()) #communicates with bot by using token file
