local M = {}
M.MB_ADDR = 0x807D0000
function M.enter()


    debug = false
    debug_keys = false
end
function M.combo_down(jp)
    return jp["Z"] and jp["L"] and jp["R"]
end
function M.get_turn_offset(jp)
    if jp["Z"] and jp["L"] then
        if jp["DPad U"] then
            return 10
        elseif jp["DPad D"] then
            return -10
        elseif jp["DPad L"] then
            return -1
        elseif jp["DPad R"] then
            return 1
        end
    end
    return 0
end
function M.r8(addr)
    return memory.read_u8(addr)
end
function M.w8(addr, value)
    memory.write_u8(addr, value)
end
function M.r16(addr)
    return mainmemory.read_u16_be(addr)
end
function M.w16(addr, value)
    mainmemory.write_u16_be(addr, value)
end
function M.write_string(addr, str)
    for i=1,#str do
        M.w8(addr + i - 1, string.byte(str, i))
    end
end

local global_addrs = {
    ["total_turns"] = 0x800CD05A,
    ["current_turn"] = 0x800CD05B,
    ["player"] = {
        [0] = {
            ["cpu_diff"] = 0x800D1109,
            ["controller"] = 0x800D110A,
            ["char"] = 0x800D110B,
            ["coins"] = 0x800D1112, --u16
            ["stars"] = 0x800D1116,
            ["turn_color"] = 0x800D1124,
            ["d1"] = 0x800CDBD2,
            ["d2"] = 0x800CDBD3,
            ["d3"] = 0x800CDBD4
        },
        [1] = {
            ["cpu_diff"] = 0x800D1141,
            ["controller"] = 0x800D1142,
            ["char"] = 0x800D1143,
            ["coins"] = 0x800D114A, --u16
            ["stars"] = 0x800D114E,
            ["turn_color"] = 0x800D115C,
            ["d1"] = 0x800CDB1E,
            ["d2"] = 0x800CDB1F,
            ["d3"] = 0x800CDB20
        },
        [2] = {
            ["cpu_diff"] = 0x800D1179,
            ["controller"] = 0x800D117A,
            ["char"] = 0x800D117B,
            ["coins"] = 0x800D1182, --u16
            ["stars"] = 0x800D1186,
            ["turn_color"] = 0x800D1194,
            ["d1"] = 0x800CDB6A,
            ["d2"] = 0x800CDB6B,
            ["d3"] = 0x800CDB6C
        },
        [3] = {
            ["cpu_diff"] = 0x800D11B1,
            ["controller"] = 0x800D11B2,
            ["char"] = 0x800D11B3,
            ["coins"] = 0x800D11BA, --u16
            ["stars"] = 0x800D11BE,
            ["turn_color"] = 0x800D11CC,
            ["d1"] = 0x800CDBB6,
            ["d2"] = 0x800CDBB7,
            ["d3"] = 0x800CDBB8
        }
    }
}
local last_offset = 0
local scene = M.r8(0x807D0000 + 8)
function M.debug_mode(ary)
    if scene == 0 then
        gui.text(10, 10, "Scene: Out of Board")
    elseif scene == 1 then
        local i = 0
        while i < 18 do
            gui.text(10, 10 + i * 10, ary[i] or "")
            i = i + 1
        end
    end
    local i = 0
    gui.text(300, 10 + i * 10, "Current Scene"..M.r16(0x000CE202))

    gui.text(200, 10, "Player 1 CPU Diff: "..tostring(M.r8(global_addrs["player"][0]["cpu_diff"])))
    gui.text(200, 20, "Player 1 Controller: "..tostring(M.r8(global_addrs["player"][0]["controller"])))
    gui.text(200, 30, "Player 1 Character: "..tostring(M.r8(global_addrs["player"][0]["char"])))
    gui.text(200, 40, "Player 2 CPU Diff: "..tostring(M.r8(global_addrs["player"][1]["cpu_diff"])))
    gui.text(200, 50, "Player 2 Controller: "..tostring(M.r8(global_addrs["player"][1]["controller"])))
    gui.text(200, 60, "Player 2 Character: "..tostring(M.r8(global_addrs["player"][1]["char"])))
    gui.text(200, 70, "Player 3 CPU Diff: "..tostring(M.r8(global_addrs["player"][2]["cpu_diff"])))
    gui.text(200, 80, "Player 3 Controller: "..tostring(M.r8(global_addrs["player"][2]["controller"])))
    gui.text(200, 90, "Player 3 Character: "..tostring(M.r8(global_addrs["player"][2]["char"])))
    gui.text(200, 100, "Player 4 CPU Diff: "..tostring(M.r8(global_addrs["player"][3]["cpu_diff"])))
    gui.text(200, 110, "Player 4 Controller: "..tostring(M.r8(global_addrs["player"][3]["controller"])))
    gui.text(200, 120, "Player 4 Character: "..tostring(M.r8(global_addrs["player"][3]["char"])))
end
function M.update()
        inv_Menu_items = {
        [0x00] = "Mushroom x ",
        [0x01] = "Skeleton Key x ",
        [0x02] = "Poison Mushroom x ",
        [0x03] = "Reverse Mushroom x ",
        [0x04] = "Cellular Shopper x ",
        [0x05] = "Warp Block x ",
        [0x06] = "Plunder Chest x ",
        [0x07] = "Bowser Phone x ",
        [0x08] = "Dueling Glove x ",
        [0x09] = "Lucky Lamp x ",
        [0x0A] = "Golden Mushroom x ",
        [0x0B] = "Boo Bell x ",
        [0x0C] = "Boo Repellant x ",
        [0x0D] = "Bowser Suit x ",
        [0x0E] = "Magic Lamp x ",
        [0x0F] = "Koopa Card x ",
        [0x10] = "Barter Box x ",
        [0x11] = "Lucky Coin x ",
        [0x12] = "Wacky Watch x "
    }
    SHRM_ADDR = M.MB_ADDR + 0x09 + 0x80 + 0x0F
    flag = false
    local jp = joypad.get(1)
    off_combo = M.get_turn_offset(jp)
    max = M.r8(M.MB_ADDR -0x01)
    if max == 0 then
        max = M.r8(global_addrs["total_turns"])
    end
    curturn = M.r8(global_addrs["current_turn"])
    if last_offset == 0 and off_combo ~= 0 then
        temp = curturn + off_combo
        if temp < 1 then
            temp = 1 
        elseif temp > max then
            temp = max
        end
        M.w8(global_addrs["current_turn"], temp)
    end
    last_offset = off_combo
    curturn = M.r8(global_addrs["current_turn"])
    if max ~= 0 then
        gui.text(10, 600, "Current turn: "..curturn.."/"..max)
    end
    down = M.combo_down(jp)
    if not debug_keys and down then
        debug = not debug
    end
    debug_keys = down

    SB_ADDR = 0x807D00C8
    inventory = {}
    for i=0,19 do
        inventory[i] = M.r8(SB_ADDR + i)

    end
    TXT_ADDR = SB_ADDR + 20
    TXT2_ADDR = TXT_ADDR + 1000
    PAGE_ADDR = TXT2_ADDR + 1000
    page = M.r8(PAGE_ADDR)
    MAP_BASE_ADDR = PAGE_ADDR + 1
    MAP2_BASE_ADDR = MAP_BASE_ADDR + 15
    if M.r8(0x807D0000 + 8) == 1 then
        menu_array = {}
        local C = 0
        for i=0,14 do
            M.w8(MAP_BASE_ADDR + i, 0xFC)
            M.w8(MAP2_BASE_ADDR + i, 0xFC)
        end
        for i=0,18 do
            if inventory[i] > 0 then
                menu_array[C] =  inv_Menu_items[i]..tostring(inventory[i])
                if C < 10 then
                    M.w8(MAP_BASE_ADDR + C, i)
                    C = C + 1
                else
                    M.w8(MAP2_BASE_ADDR + (C - 10), i)
                    C = C + 1
                end
            end
        end
        if C > 9 then
            M.w8(MAP_BASE_ADDR + 10, 0xFD)
            M.w8(MAP_BASE_ADDR + 11, 0xFE)
            M.w8(MAP_BASE_ADDR + 12, 0xFF)
            M.w8(MAP2_BASE_ADDR + C - 10, 0xFD)
            M.w8(MAP2_BASE_ADDR + C - 9, 0xFE)
            M.w8(MAP2_BASE_ADDR + C - 8, 0xFF)
        else
            if M.r8(MAP_BASE_ADDR) ~= 0xFC then
                M.w8(MAP_BASE_ADDR + C, 0xFE)
                M.w8(MAP_BASE_ADDR + C + 1, 0xFF)
            end
        end
    end


    if debug then
        M.debug_mode(menu_array)
    end

end

return M