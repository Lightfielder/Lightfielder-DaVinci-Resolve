--[[--
Lightfielder PathMap Setup.lua 2026-09-02 07.10 PM (UTC -3)

Setting up Lightfielder for the first time is a 2 step process.

1. Launch Resolve Studio and navigate to the Fusion page.

2. Drag the 'Lightfielder PathMap Setup.lua' script from your desktop folder into the Fusion node graph or Console window. A Fusion preference called a PathMap will be configured automatically for Lightfielder using this script.

Note: You can also copy the contents of this script and manually paste it into the text entry line at the bottom of the Console window to run the script if drag-and-drop doesn't work for you.

--]]--

print('[Lightfielder PathMap Setup]')

-- Add the platform specific folder slash character
osSeparator = package.config:sub(1,1)

-- Set the customized Lightfielder PathMap
local home = os.getenv([[HOME]]) or os.getenv([[USERPROFILE]]) 
local lightfielder_root = app:MapPath(tostring(home) .. osSeparator .. [[Lightfielder]] .. osSeparator)
app:SetPrefs([[Global.Paths.Map.Lightfielder:]], lightfielder_root)
local userpath = app:GetPrefs([[Global.Paths.Map.UserPaths:]])
if not userpath:find([[Lightfielder:Resolve]]) then
    userpath = userpath .. [[;Lightfielder:Resolve]]
    app:SetPrefs([[Global.Paths.Map.UserPaths:]], userpath)
end

app:SavePrefs()

print([[[Lightfielder: PathMap] ']] .. tostring(app:GetPrefs([[Global.Paths.Map.Lightfielder:]])) .. [[']])
print([[Lightfielder is now connected, restart Resolve Studio to finish the installation.]])
app:DoAction('Console_Show', {Show = true})
