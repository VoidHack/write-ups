from PIL import Image

def bin_return(dec):
    return(str(format(dec,'b')))

def bin_8bit(dec):
    return(str(format(dec,'08b')))

def convert_32bit(dec):
    return(str(format(dec,'032b')))

def convert_64bit(dec):
    return(str(format(dec,'064b')))

def hex_return(dec):
    return expand(hex(dec).replace('0x','').replace('L',''))

def dec_return_bin(bin_string):
    return(int(bin_string,2))

def dec_return_hex(hex_string):
    return(int(hex_string,16))

def some_LP(l,n):
    l1=[]
    j=0
    k=n
    while k<len(l)+1:
        l1.append(l[j:k])
        j=k
        k+=n
    return(l1)

def rotate_right(bit_string,n):
    bit_list = list(bit_string)
    count=0
    while count <= n-1:
        list_main=list(bit_list)
        var_0=list_main.pop(-1)
        list_main=list([var_0]+list_main)
        bit_list=list(list_main)
        count+=1
    return(''.join(list_main))

def shift_right(bit_string,n):
    bit_list=list(bit_string)
    count=0
    while count <= n-1:
        bit_list.pop(-1)
        count+=1
    front_append=['0']*n
    return(''.join(front_append+bit_list))

def addition(input_set):
    value=0
    for i in range(len(input_set)):
        value+=input_set[i]
    mod_32 = 4294967296
    return(value%mod_32)

def str_xor(s1,s2):
    return ''.join([str(int(i)^int(j)) for i,j in zip(s1,s2)])

def str_and(s1,s2):
    return ''.join([str(int(i)&int(j)) for i,j in zip(s1,s2)])

def str_not(s):
    return ''.join([str(int(i)^1) for i in s])

def not_and_and_xor(x,y,z):
    return(str_xor(str_and(x,y),str_and(str_not(x),z)))

def and_and_and_xor_xor(x,y,z):
    return(str_xor(str_xor(str_and(x,y),str_and(x,z)),str_and(y,z)))

def some_e0(x):
    return(str_xor(str_xor(rotate_right(x,2),rotate_right(x,13)),rotate_right(x,22)))

def some_e1(x):
    return(str_xor(str_xor(rotate_right(x,6),rotate_right(x,11)),rotate_right(x,25)))

def some_s0(x):
    return(str_xor(str_xor(rotate_right(x,7),rotate_right(x,18)),shift_right(x,3)))

def some_s1(x):
    return(str_xor(str_xor(rotate_right(x,17),rotate_right(x,19)),shift_right(x,10)))

def expand(s):
	return '0'*(8-len(s))+s

def get_pixels_list(filename):
    im = Image.open(filename)
    return list(im.getdata())

def data_encrypted(list_of_pixels):
	data = ''
	for i in list_of_pixels:
		d = ''.join([chr(j) for j in i])
		d = encryption(d)
		data += ''.join(d)
		print len(data)
	return data

def message_pad(bit_list):
    pad_one = bit_list + '1'
    pad_len = len(pad_one)
    k=0
    while ((pad_len+k)-448)%512 != 0:
        k+=1
    back_append_0 = '0'*k
    back_append_1 = convert_64bit(len(bit_list))
    return(pad_one+back_append_0+back_append_1)

def message_bit_return(string_input):
    bit_list=[]
    for i in range(len(string_input)):
        bit_list.append(bin_8bit(ord(string_input[i])))
    return(''.join(bit_list))

def message_pre_pro(input_string):
    bit_main = message_bit_return(input_string)
    return(message_pad(bit_main))

def message_parsing(input_string):
    return(some_LP(message_pre_pro(input_string),32))

def message_schedule(index,w_t):
    new_word = convert_32bit(addition([int(some_s1(w_t[index-2]),2),int(w_t[index-7],2),int(some_s0(w_t[index-15]),2),int(w_t[index-16],2)]))
    return(new_word)

initial=['6a09e667','bb67ae85','3c6ef372','a54ff53a','510e527f','9b05688c','1f83d9ab','5be0cd19']

values=['428a2f98','71374491','b5c0fbcf','e9b5dba5','3956c25b','59f111f1','923f82a4','ab1c5ed5','d807aa98','12835b01','243185be','550c7dc3','72be5d74','80deb1fe','9bdc06a7','c19bf174','e49b69c1','efbe4786','0fc19dc6','240ca1cc','2de92c6f','4a7484aa','5cb0a9dc','76f988da','983e5152','a831c66d','b00327c8','bf597fc7','c6e00bf3','d5a79147','06ca6351','14292967','27b70a85','2e1b2138','4d2c6dfc','53380d13','650a7354','766a0abb','81c2c92e','92722c85','a2bfe8a1','a81a664b','c24b8b70','c76c51a3','d192e819','d6990624','f40e3585','106aa070','19a4c116','1e376c08','2748774c','34b0bcb5','391c0cb3','4ed8aa4a','5b9cca4f','682e6ff3','748f82ee','78a5636f','84c87814','8cc70208','90befffa','a4506ceb','bef9a3f7','c67178f2']

def encryption(input_string):
    w_t=message_parsing(input_string)
    a=convert_32bit(dec_return_hex(initial[0]))
    b=convert_32bit(dec_return_hex(initial[1]))
    c=convert_32bit(dec_return_hex(initial[2]))
    d=convert_32bit(dec_return_hex(initial[3]))
    e=convert_32bit(dec_return_hex(initial[4]))
    f=convert_32bit(dec_return_hex(initial[5]))
    g=convert_32bit(dec_return_hex(initial[6]))
    h=convert_32bit(dec_return_hex(initial[7]))
    for i in range(0,64):
        if i <= 15:
            t_1=addition([int(h,2),int(some_e1(e),2),int(not_and_and_xor(e,f,g),2),int(values[i],16),int(w_t[i],2)])
            t_2=addition([int(some_e0(a),2),int(and_and_and_xor_xor(a,b,c),2)])
            h=g
            g=f
            f=e
            e=addition([int(d,2),t_1])
            d=c
            c=b
            b=a
            a=addition([t_1,t_2])
            a=convert_32bit(a)
            e=convert_32bit(e)
        if i > 15:
            w_t.append(message_schedule(i,w_t))
            t_1=addition([int(h,2),int(some_e1(e),2),int(not_and_and_xor(e,f,g),2),int(values[i],16),int(w_t[i],2)])
            t_2=addition([int(some_e0(a),2),int(and_and_and_xor_xor(a,b,c),2)])
            h=g
            g=f
            f=e
            e=addition([int(d,2),t_1])
            d=c
            c=b
            b=a
            a=addition([t_1,t_2])
            a=convert_32bit(a)
            e=convert_32bit(e)
    value_0 = addition([dec_return_hex(initial[0]),int(a,2)])
    value_1 = addition([dec_return_hex(initial[1]),int(b,2)])
    value_2 = addition([dec_return_hex(initial[2]),int(c,2)])
    value_3 = addition([dec_return_hex(initial[3]),int(d,2)])
    value_4 = addition([dec_return_hex(initial[4]),int(e,2)])
    value_5 = addition([dec_return_hex(initial[5]),int(f,2)])
    value_6 = addition([dec_return_hex(initial[6]),int(g,2)])
    value_7 = addition([dec_return_hex(initial[7]),int(h,2)])
    value = (hex_return(value_0),hex_return(value_1),hex_return(value_2),hex_return(value_3),hex_return(value_4),hex_return(value_5),hex_return(value_6),hex_return(value_7))
    return(value)

list_pixels = get_pixels_list('./flag3.png')
data = data_encrypted(list_pixels)
f = open('./encrypted3.txt','w')
f.write(data)
f.close()