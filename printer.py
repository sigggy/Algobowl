def printer(lightmap, nummap, retMap, map):
    for i in range(len(lightmap)):
        for j in range(len(lightmap[0])):
            if lightmap[i][j]:
                print(lightmap[i][j].__str__(), end= ' ')
                continue 
            print(lightmap[i][j], end = ' ')
        print()
    print()

    for i in range(len(lightmap)):
        for j in range(len(lightmap[0])):
            if lightmap[i][j]:
                print(f'light map at {lightmap[i][j].__str__()} with {lightmap[i][j].collisions} collisions')
                for element in lightmap[i][j].neighbors:
                    print(f' -collision at {element.__str__()}')
    
                print()
        print()
        
    for i in range(len(nummap)):
        for j in range(len(nummap[0])):
            if nummap[i][j]:
                print(nummap[i][j].__str__(), end= ' ')
                continue 
            print(nummap[i][j], end = ' ')
        print()
    print()

    for i in range(len(nummap)):
        for j in range(len(nummap[0])):
            if nummap[i][j]:
                print(f'light map at {nummap[i][j].__str__()}')
                for element in nummap[i][j].adjacent_lights:
                    print(f' -adajcent at {element.__str__()}')
    
                print()
        print()

    for i in range (len(retMap)):
        for j in range(len(retMap[0])):
            if retMap[i][j]:
                print(retMap[i][j].__str__(), end= ' ')
                continue 
            print(retMap[i][j], end = ' ')
        print()
    print()

    for i in range (len(map)):
        for j in range(len(map[0])):
            if map[i][j]:
                print(map[i][j].__str__(), end= ' ')
                continue 
            print(map[i][j], end = ' ')
        print()
    print()
