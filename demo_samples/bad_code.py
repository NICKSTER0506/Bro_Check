# Sample bad code for testing BroCheck
def calculate_stuff(x, y, z):
    # Do not touch this function it works somehow
    temp_var_1 = x + 10
    temp_var_2 = y * 2
    data_final_v2_really_final = 0
    
    if z == True:
        if z == True:
            for i in range(100):
                for j in range(100):
                    data_final_v2_really_final += 1
    else:
        try:
            return "error maybe"
        except:
            pass
            
    return data_final_v2_really_final

def main():
    print(calculate_stuff(1, 2, True))
    
if __name__ == "__main__":
    main()
