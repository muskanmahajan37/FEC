#######################################################
### NIEZAWODNOSC I DIAGNOSTYKA UKLADOW CYFROWYCH 2  ###
###        Grzegorz Pelc i Jakub Pawleniak          ###
###                 GRUPA 9                         ###
#######################################################
import random
import math
import os
import matplotlib.pyplot as plt
import numpy
#########  PARAMETRY  ###########
# generator bitow
generator_function  = True #aby wprowadzic wlasna wartosc bitow zmien wartosc zmiennej funkcja z True na False
user_bits = [0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0] #w przypadku generator_function = False: tutaj wpisz wlasne bity w formie listy
bits_length = 1000 #w przypadku generator_function = True: wpisz tutaj dlugosc listy losowanych bitow
chance = 50 #w przypadku generator_function = True: procentowa szansa na wylosowanie 1. Podaj w zakresie od 0 do 100 (wartosc calkowita)

# Generator pakietow
packet_length = 8 #min 4, koduje tylko dla długości 2^n

#Symulacja przesyłu
error_chance = 4 # % szansy na przeklamanie. Podaj w zakresie od 0 do 100, senosownie to przedział <2,5>

#Wybor Funckji  True- Hamming   False- CRC
co_chcesz = True

#Wielomian CRC
crc = [1,0,0,1,0,1]    # 0x12

#Parametry do eksperymentu (2 i 3 etap)
ilosc_symulacji = 10000 #ilość przeprowadzonych symulacji przesylu danych

#GENERATOR BITÓW
def bits_generator():
    bits = []
    if generator_function == True:
        index = 0
        while index < bits_length:
            index += 1
            if random.randint(0, 100) <= chance:
                bits.append(1)
            else:
                bits.append(0)
    else:
        bits = user_bits
    return bits
####################################################################
#GENERATOR PAKIETOW
def make_packets(bits):
    packets = []
    packet = []
    index = 0

    while index < (len(bits)):
        if len(packet) < packet_length:
            bit = bits[index]
            packet.append(bit)
            index += 1
        else:
            packets.append(packet)
            packet = []
    if len(packet) == packet_length:
        packets.append(packet)
    else:
        for i in range((packet_length - (len(packet)))):
            packet.append(0)
        packets.append(packet)
    return packets
####################################################################
#kodowanie pakietow (dodawanie zer do wiadomosci)
def crc_coder(packet):
    helper1 = 0
    while helper1 < (len(crc)-1):
        packet.append(0)
        helper1 += 1
    return packet
###################################################################

#liczenie sumy kontrolnej (zamiana "dokodowanych" zer na odpowiednią sumę kontrolną)
def crc_maker(packet):
    packet1 = []
    for i in range (len(packet)):
        packet1.append(packet[i])
    for w in range(len(packet1) - (len(crc) - 1)):
        if packet1[w] == 1:
            for e in range(len(crc)):
                operator_co_mi_pomoze = w + e
                # print (operator_co_mi_pomoze)
                if operator_co_mi_pomoze < len(packet1):
                    packet1[operator_co_mi_pomoze] = packet1[operator_co_mi_pomoze] ^ crc[e]
    check_value = []
    helperro = (len(packet1) - (len(crc) - 1))
    # print (helper2)
    # print(check_value)
    while helperro < (len(packet1)):
        check_value.append(packet1[helperro])
        helperro += 1
    return check_value
###############################################################
#kodowanie wiadomosci (dodanie obliczonego CRC)
def code_message(packets):
    for packet in packets:
        work_packet = crc_coder(packet)
        check_value = crc_maker(work_packet)
        #print (check_value)
        check_value_iterator = (len(packet) - (len(crc)-1))
        z=0
        while check_value_iterator < (len(work_packet)):
            packet[check_value_iterator] = check_value[z]
            check_value_iterator+=1
            z+=1
    return packets
##############################################################
#symulacja przesyłania
def transmission_simulation (packets):
    new_packets = []
    temp = 0
    for packet in packets:
        new_packet = []
        for bit in packet:
            if random.randint(1, 100) <= error_chance:
                temp = bool(bit)
                temp = not(temp)
                temp = int(temp)
                new_packet.append(temp)
            else:
                new_packet.append(bit)
                continue
        new_packets.append(new_packet)
    return new_packets
###############################################################
#zwraca 0 jak jest git 1 jak jest jedna jedynka(magia naprawiania crc) i 2 jak wiecej jedynek
def check(packet):
    check_value = crc_maker(packet)
    #print ("TU JESTEM I SPRAWDZAM ILOSC JEDYNEK W KODZIE KONTROLNYM")
    #print (check_value)
    unos = 0
    for i in range(len(check_value)):
        if check_value[i] == 1:
            unos += 1
    if unos == 0:
        return 0
    if unos == 1:
        return 1
    else:
        return 2
#################################################################
def przesun1 (packet):
    temp = packet [len(packet)-1]                       # PRZESUWANIE W JEDNĄ STRONĘ
    del packet[len(packet)-1]
    packet.insert(0,temp)
    return packet
#################################################################
def przesun2 (packet):
    temp = packet [0]
    del packet[0]                                       # PRZESUWANIE W DRUGĄ STRONĘ
    packet.append(temp)
    return packet
##################################################################
#naprawiator
def repair (packet,check_code):
    if check_code == 1:                                 # NAPRAWIANIE SUMY KONTROLNEJ
        check_value = crc_maker(packet)
        #print("TU JESTEM i naprawiam bo jest jedna jedynka ")
        for j in range (len(check_value)):
            helper4 = len(packet) - (len(crc)-1) + j
            if check_value[j] == 1:
                packet[helper4] = packet[helper4] ^ 1
        return packet
    if check_code == 2:
        for a in range(1,len(packet)):
            #print("TU JESTEM i przesuwam aż bedzie jedna jedyneczka ktorej pragne")
            #print(a)
            packet = przesun1(packet)
            #print (packet)
            kontrolka = check(packet)
            if(kontrolka == 1):
                packet = repair(packet,1)
                while a > 0:
                    packet = przesun2(packet)
                    a -=1
                return packet
           # else:
                #print("JESZCZE NIE JEST FAJNIE :(")
        while a > 0:
            packet = przesun2(packet)
            a -= 1
        return packet
################################################################
def decode_message(packets):
    packets_ready = []
    for packet in packets:
        kontrolka = (check(packet))
        if(kontrolka) == 0:   #Pakiet poprawny

            i = len(crc)-1
            while i > 0:
                del packet[len(packet)-1]
                i-=1
            packet.insert(0,'1')
            packets_ready.append(packet)

        else:
            packet = repair(packet,kontrolka)
            if (check(packet) == 0):
                i = len(crc) - 1
                while i > 0:
                    del packet[len(packet) - 1]
                    i -= 1
                packet.insert(0, '2')
                packets_ready.append(packet)
            else:
                i = len(crc) - 1
                while i > 0:
                    del packet[len(packet) - 1]
                    i -= 1
                packet.insert(0, '3')
                packets_ready.append(packet)
    return packets_ready
################################################################ TERAZ HAMINNGIEM
def to_binary_table(x):
    temp = bin(x)[2:]
    binary_table = []
    for i in temp:
        i = int(i)
        binary_table.append(i)
    return binary_table

def bin_table_to_decimal (lst):
    power = len(lst) - 1
    decimal = 0
    for bin in lst:
        if bin == 1:
            decimal += (pow(2, power))
        power -= 1
    return decimal


def longest_list_in_list(lst): #funkcja zwracajaca wartosc dlugosci najdluzszej listy w liście list
    temp = []
    for lst_1 in lst:
        temp.append(len(lst_1))
    sorted(temp)
    temp.reverse()
    return  temp[0]

def Hamming_code (lst):
    i = 0
    temp = []
    temp1 = 0
    index = longest_list_in_list(lst)
    while i < index:
        for lst1 in lst:
            if lst1[i] == 1:
                temp1 += 1
            else:
                continue
        if (temp1 % 2 == 0):
            temp.append(0)
        else:
            temp.append(1)
        temp1 = 0
        i += 1
    return temp



def coding_Hamming(packets):
    coded_packets = []
    for packet in packets:
        packet.reverse()
        place_of_1 = []
        place_of_1_bin = []
        index = 1
        packet.insert(0, 'tu')
        for x in range(1,((math.ceil(math.sqrt(len(packet)))) + packet_length)):
            if math.log2(x+1).is_integer():
                packet.insert(x, 'tu')
            else:
                continue
        for bit in packet:
            if bit == 1:
                place_of_1.append(index)
                index += 1
            else:
                index += 1
        if place_of_1 == []:
            place_of_1.append(0)
        for place in range(len(place_of_1)):
            temp = to_binary_table(place_of_1[place])
            place_of_1_bin.append(temp)
            temp1 = packet.count ('tu')
        for place in place_of_1_bin:
            while len(place) < temp1:
                place.insert(0, 0)
        temp2 = Hamming_code(place_of_1_bin)
        temp2.reverse()
        i = 0
        i_code = 0
        while packet.count ('tu') != 0:
            if packet[i] == 'tu':
                packet.pop(i)
                packet.insert(i, temp2[i_code])
                i_code += 1
                i += 1
            else:
                i += 1
        packet.reverse()
        coded_packets.append(packet)

    return coded_packets

#Dekodowanie sygnału

def delete_code (packet):
    index = len(packet) - 1
    while index >= 0:
        if (math.log2(index+1).is_integer()) or (index == 0):
            packet.pop(index)
            index -= 1
        else:
            index -= 1
            continue
    return packet

def fix_packet (packet, place):
    index = 1
    while index <= len(packet):
        if index == place:
            temp = packet[index - 1]
            temp1 = not(bool(temp))
            packet.pop(index - 1)
            packet.insert((index - 1), int(temp1))
            index += 1
        else:
            index += 1
            continue
    return packet

def decoding_Hamming(packets):
    decoded_packets = []
    for packet in packets:
        place_of_one = []
        place_of_one_bin = []
        index = 1
        packet.reverse()
        for bit in packet:
            if bit == 1:
                place_of_one.append(index)
                index += 1
            else:
                index += 1
        if place_of_one == []:
            place_of_one.append(0)
        for place in place_of_one:
            place_of_one_bin.append(to_binary_table(place))
        temp1 = longest_list_in_list(place_of_one_bin)
        for place in place_of_one_bin:
            while len(place) < temp1:
                place.insert(0, 0)
        code = Hamming_code(place_of_one_bin)
        place_of_mistake = bin_table_to_decimal(code)
        if place_of_mistake == 0:
            delete_code(packet)
            packet.append('1') #dodanie znacznika opcji (1 dla transmisji bez wykrytego bledu)
        elif place_of_mistake <= len(packet):
            packet = fix_packet(packet, place_of_mistake)
            delete_code(packet)
            packet.append('2') #dodanie znacznika opcji (2 dla transmisji z wykrytym i poprawionym bledem)
            #tutaj jest problem, dla 2 bledow wykrywa i poprawia jeden kompletnie inny (poprawny) bit
        elif place_of_mistake > len(packet):
            delete_code(packet)
            packet.append('3') #dodanie znacznika opcji (3 wykrywa blad, ktorego nie potrafi naprawic)
        packet.reverse()
        decoded_packets.append(packet)
    return decoded_packets


def hamming(packets):
    #print ("CZESC")
    if (packet_length < 4) or (not(math.log2(packet_length).is_integer())):
        print("NIEOBSLUGIWALNA DLUGOSC PAKIETU")
        exit()


    coded_packets = coding_Hamming(packets)
    recived_packets = transmission_simulation(coded_packets)

    control_packets_recived = []
    for j in range(len(recived_packets)):  # pakiety zapisane do późniejszej kontroli
        control_packets_recived.append(recived_packets[j])

    decoded_packets = decoding_Hamming(recived_packets)
    #print(decoded_packets)
    return decoded_packets

def crc_dzida(packets):


    packets_to_send = code_message(packets)
    #print("Zakodowane:")
    #print(packets_to_send)
    packets_recevied = transmission_simulation(packets_to_send)
    #print("Po zaszumieniu:")
    #print(packets_recevied)
    packets_ready = decode_message(packets_recevied)
    #print("FINALNIE:")
    #print(packets_ready)
    return packets_ready

def four_options (packets, org_packets):
    options = [0,0,0,0] #Cztery opcje: i = 0 -> pakiet przeszedł dobrze i został tak odczytany
                        #              i = 1 -> pakiet przyszedł z błędem i został wykryty i poprawnie naprawiony
                        #              i = 2 -> pakiet przyszedł z błędem, został wykryty, ale nienaprawiony
                        #              i = 3 -> pakiet przyszedł z błędem, który nie został lub został błędnie wykryty
    i = 0
    while i < len(packets):
        packet = packets[i]
        org_packet = org_packets[i]
        index = 0
        blad = 0
        while index < packet_length:
            if packet[index + 1] == org_packet[index]:
                index += 1
            else:
                blad += 1
                index += 1
        if (packet [0] == '1') and (blad == 0):
            options[0] += 1
        elif (packet [0] == '2') and (blad == 0):
            options[1] += 1
        elif (packet [0] == '3') and (blad != 0):
            options[2] += 1
        else:
            options[3] += 1
        i += 1
    return options





def main():

    #print("DZIEN DOBRY")

    bits = bits_generator()
    packets = make_packets(bits)
    #print("Pakiety:")
    #print(packets)
    packets_original = []
    packet_original = []
    for i in packets: # pakiety zapisane do późniejszej analizy
        packet_original = []
        for j in i:
            packet_original.append(j)
        packets_original.append(packet_original)


    if co_chcesz == True:
        pakieciki = hamming(packets)
        #print(pakieciki)
    else:
        pakieciki = crc_dzida(packets)
        #print(pakieciki)

    wynik = four_options(pakieciki, packets_original)
    #print(wynik)
    return wynik


#Tu zaczyna się 2. etap

def utworz_folder_na_wyniki():
    nr_testu = 1
    while os.path.exists("Test_{}".format(nr_testu)):
        nr_testu += 1
        continue
    os.mkdir("Test_{}".format(nr_testu))
    return nr_testu


def experiment ():
    wynik_eksperymentu = []
    for i in range(ilosc_symulacji):
        wynik_eksperymentu.append(main())
    return wynik_eksperymentu


def srednia (wynik_eks, nr_testu):
    print(wynik_eks)
    ilosc_pakietow = int(bits_length/packet_length*ilosc_symulacji)
    opcja_1 = 0
    opcja_2 = 0
    opcja_3 = 0
    opcja_4 = 0
    opcje = []
    kolorki = ['#4af011','#3c8d20','#F06B96','#ed0909']
    nazwy = ['Dotarł bez zakłóceń', 'Naprawiono poprawnie', 'Wykryty bład, bez naprawy', 'Błędnie naprawione']
    for eksperyment in wynik_eks:
        opcja_1 += eksperyment[0] #zliczanie ile kazdej z opcji było łącznie we wszystkich powtórzeniach symulacji
        opcja_2 += eksperyment[1]
        opcja_3 += eksperyment[2]
        opcja_4 += eksperyment[3]
    opcje.append(opcja_1)
    opcje.append(opcja_2)
    opcje.append(opcja_3)
    opcje.append(opcja_4)
    plt.pie(opcje,
            autopct= '%1.2f%%',
            colors= kolorki,
            startangle= 90)
    plt.title('Wykres średniej')
    plt.legend(nazwy, loc="best")
    plt.savefig("Test_{}/Wykres_sredniej.png".format(nr_testu))
    plt.show()

    file = open("Test_{}/Wyniki średniej.txt".format(nr_testu), mode= "a+")
    file.write("Ilość pakietów łącznie: %s\n" %ilosc_pakietow)
    file.write("Ilość pakietów przesłanych bez błędów: %s\n" %opcja_1)
    file.write("Ilość pakietów poprawnie naprawionych: %s\n" % opcja_2)
    file.write("Ilość pakietów z wykrytym błędem bez naprawy: %s\n" % opcja_3)
    file.write("Ilość pakietów błędnie wykrytych: %s\n" % opcja_4)
    file.close()

def five_num_summary(wyniki_exp,nr_testu):
    big_data =[]
    for j in range(len(wyniki_exp[0])):
        data = []
        for experiment in wyniki_exp:
            data.append(experiment[j])
        kwartyle = five_num_sum_counter(data)
        big_data.append(kwartyle)

        print("Kwartyle dla: ")
        print(j)
        print(kwartyle[0])
        print(kwartyle[1])
        print(kwartyle[2])
        print(kwartyle[3])
        print(kwartyle[4])
    index = 0
    file = open("Test_{}/Wyniki statysyki pięciopunktowej.txt".format(nr_testu), mode="a+")
    for kwartyle in big_data:
        file.write('Kwartyle dla Sytuacji: %s\n' %index)

        file.write("Min: %s\n" % kwartyle[0])
        file.write("Q1: %s\n" % kwartyle[1])
        file.write("Med: %s\n" % kwartyle[2])
        file.write("Q3: %s\n" % kwartyle[3])
        file.write("Max: %s\n" % kwartyle[4])
        index+=1
    file.close()

def five_num_sum_counter(data):
    fivenumsumtab = numpy.quantile(data, [0, .25, .50, .75, 1])
    return fivenumsumtab

def boxplot(wyniki_exp,nr_testu):
    bigger_data = []
    for j in range(len(wyniki_exp[0])):
        data = []
        for experiment in wyniki_exp:
            data.append(experiment[j])
        bigger_data.append(data)
    box=plt.boxplot(bigger_data,patch_artist=True, labels = ['Sytuacja 0','Sytuacja 1','Sytuacja 2','Sytuacja 3'])
    plt.title('Wykres pudełkowy')
    colors = ['#4af011','#3c8d20','#F06B96','#ed0909']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.savefig("Test_{}/Wykres_pudełkowy.png".format(nr_testu), dpi=350)
    plt.show()

def histogramik (wynik_eks, nr_testu):
    opcja_1 = []
    opcja_2 = []
    opcja_3 = []
    opcja_4 = []
    for eksperyment in wynik_eks:
        opcja_1.append(eksperyment[0]) #zliczanie ile kazdej z opcji było łącznie we wszystkich powtórzeniach symulacji
        opcja_2.append(eksperyment[1])
        opcja_3.append(eksperyment[2])
        opcja_4.append(eksperyment[3])
    #Histogram opcji 1
    plt.hist(opcja_1, edgecolor = 'black', alpha = 0.5)
    plt.title('Histogram - opcja 1')
    plt.grid(True)
    plt.savefig("Test_{}/Histogram1.png".format(nr_testu), dpi=350)
    plt.show()
    #Histogram opcji 2
    plt.hist(opcja_2, edgecolor = 'black', alpha = 0.5)
    plt.title('Histogram - opcja 2')
    plt.grid(True)
    plt.savefig("Test_{}/Histogram2.png".format(nr_testu), dpi=350)
    plt.show()
    #Histogram opcji 3
    plt.hist(opcja_3, edgecolor = 'black', alpha = 0.5)
    plt.title('Histogram - opcja 3')
    plt.grid(True)
    plt.savefig("Test_{}/Histogram3.png".format(nr_testu), dpi=350)
    plt.show()
    #Histogram opcji 4
    plt.hist(opcja_4, edgecolor = 'black', alpha = 0.5)
    plt.title('Histogram - opcja 4')
    plt.grid(True)
    plt.savefig("Test_{}/Histogram4.png".format(nr_testu), dpi=350)
    plt.show()

test = utworz_folder_na_wyniki()
wyniki = experiment()

file = open("Test_{}/Parametry eksperymentu.txt".format(test), mode="a+")
if (co_chcesz):
    file.write("Algorytm: Hamming \n")
else:
    file.write("Algorytm: CRC \n")

file.write("Ilość bitów: %s\n" % bits_length)
file.write("Wielkość pakietu: %s\n" % packet_length)
file.write("Ilosc symulacji: %s\n" % ilosc_symulacji)
file.write("Szansa przekłamania(w procentach): %s\n" % error_chance)

file.close()

srednia(wyniki, test)
five_num_summary(wyniki,test)
boxplot(wyniki,test)
histogramik(wyniki, test)
