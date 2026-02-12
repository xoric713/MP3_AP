local function add_local_path()
    local source = debug.getinfo(1, "S").source
    if source:sub(1, 1) == "@" then
        local dir = source:sub(2):match("^(.*[\\/])")
        if dir and not package.path:find(dir, 1, true) then
            package.path = package.path .. ";" .. dir .. "?.lua;" .. dir .. "?/init.lua"
        end
    end
end

add_local_path()
local common = require("MP3common")

local BOARDS = {
    [0] = require("aptestworld.board"),
}
local active_name = nil
local active_board = nil

local M = {}
M.MB_ADDR = 0x807D0000
local function get_board()
    return common.r8(M.MB_ADDR + 0x04)
end

local function load_board(b)
    active_name = b
    active_board = BOARDS[b]

    if active_board and active_board.enter then
        active_board.enter()
    end
end

common.enter()
function M.update()
    common.update()
    local board = get_board()
    if board ~= active_name then
        load_board(board)
    end

    if active_board and active_board.update then
        active_board.update()
    end
end

return M