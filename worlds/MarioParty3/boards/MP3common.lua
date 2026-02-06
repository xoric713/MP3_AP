local M = {}
M.MB_ADDR = 0x807D0000
function M.enter()
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

    debug = false
    debug_keys = false

end
function M.combo_down(jp)
    return jp["Z"] and jp["L"] and jp["R"]
end
function M.r8(addr)
    return memory.read_u8(addr)
end
function M.w8(addr, value)
    memory.write_u8(addr, value)
end
function M.write_string(addr, str)
    for i=1,#str do
        M.w8(addr + i - 1, string.byte(str, i))
    end
end
function M.update()
    jp = joypad.get(1)
    down = M.combo_down(jp)
    if not debug_keys and down then
        debug = not debug
    end
    debug_keys = down

    SB_ADDR = 0x807E0000
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
    if M.r8(0x807D0000 + 8) == 1 or flag == false then
        flag = true
        local menu_array = {}
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
        gui.text(10, 10, M.r8(MAP_BASE_ADDR + 0))
        gui.text(10, 20, M.r8(MAP_BASE_ADDR + 1))
        gui.text(10, 30, M.r8(MAP_BASE_ADDR + 2))
        gui.text(10, 40, M.r8(MAP_BASE_ADDR + 3))
        gui.text(10, 50, M.r8(MAP_BASE_ADDR + 4))
        gui.text(10, 60, M.r8(MAP_BASE_ADDR + 5))
        gui.text(10, 70, M.r8(MAP_BASE_ADDR + 6))
        gui.text(10, 80, M.r8(MAP_BASE_ADDR + 7))
        gui.text(10, 90, M.r8(MAP_BASE_ADDR + 8))
        gui.text(10, 100, M.r8(MAP_BASE_ADDR + 9))
        gui.text(10, 110, M.r8(MAP_BASE_ADDR + 10))
        gui.text(10, 120, M.r8(MAP_BASE_ADDR + 11))
        gui.text(10, 130, M.r8(MAP_BASE_ADDR + 12))
        gui.text(10, 140, M.r8(MAP_BASE_ADDR + 13))
        gui.text(10, 150, M.r8(MAP_BASE_ADDR + 14))
        gui.text(10, 160, M.r8(MAP_BASE_ADDR + 15))
        gui.text(10, 170, M.r8(MAP_BASE_ADDR + 16))
        gui.text(10, 180, M.r8(MAP_BASE_ADDR + 17))
        gui.text(10, 190, M.r8(MAP_BASE_ADDR + 18))
        gui.text(10, 200, M.r8(MAP_BASE_ADDR + 19))
        gui.text(10, 210, M.r8(MAP_BASE_ADDR + 20))
        gui.text(10, 220, M.r8(MAP_BASE_ADDR + 21))
        gui.text(10, 230, M.r8(MAP_BASE_ADDR + 22))
        gui.text(10, 240, M.r8(MAP_BASE_ADDR + 23))
        gui.text(10, 250, M.r8(MAP_BASE_ADDR + 24))
        gui.text(10, 260, M.r8(MAP_BASE_ADDR + 25))
        gui.text(10, 270, M.r8(MAP_BASE_ADDR + 26))
        gui.text(10, 280, M.r8(MAP_BASE_ADDR + 27))
        gui.text(10, 290, M.r8(MAP_BASE_ADDR + 28))
        gui.text(10, 300, M.r8(MAP_BASE_ADDR + 29))
        gui.text(10, 310, M.r8(MAP_BASE_ADDR + 30))
    end
end

return M