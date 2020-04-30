require "discordrb"
TOKEN = 'Njk5NTk5'
CLIENT_ID = 699599071115214909

bot = Discordrb::Commands::CommandBot.new(
token: TOKEN,
client_id: CLIENT_ID,
prefix:'vc/'
)


bot.voice_state_update do |event|
    user = event.user.name

    
    if event.channel == nil then
        channel_name = event.old_channel.name

        bot.send_message("#ログ", "#{user}が#{channel_name}から出た")
    else
        channel_name = event.channel.name

        bot.send_message("#ログ", "#{user}が#{channel_name}に入った")
    end
end

bot.command :create do |event|
  event.channel_create({type: 2,topic: "Test"})
end

# botを起動
bot.run
