#genetic algorithm method to get tags (performance too slow unfortunately)

from os.path import commonprefix
from functools import partial, reduce
from itertools import chain
from typing import Iterator
import time
import Utils
import random as rand
import copy

def ngram(seq: str, n: int) -> Iterator[str]:
    return (seq[i: i+n] for i in range(0, len(seq)-n+1))

def allngram(seq: str, minn=1, maxn=None) -> Iterator[str]:
    lengths = range(minn, maxn+1) if maxn else range(minn, len(seq))
    ngrams = map(partial(ngram, seq), lengths)
    return set(chain.from_iterable(ngrams))

def commonaffix(group: list[str]) -> tuple[bool, str]:
    maxn = min(map(len, group))
    seqs_ngrams = map(partial(allngram, maxn=maxn), group)
    intersection = reduce(set.intersection, seqs_ngrams)
    try:
        check_presub = sorted(intersection, key=len, reverse=True)
        for sub in check_presub:
            if all([i.startswith(sub) or i.endswith(sub) for i in group]):
                return True, sub

        return False, ""
    except:
        return False, ""

class GenAlgo:
    def __init__(self, player_list, num_teams, per_team, generations = 125, size = 25, mut_rate = 0.1, top_select = 3): #didn't really tune these hyperparameters
        self.size = size
        self.generations = generations
        self.mut_rate = mut_rate
        self.top_select = top_select
        self.players = player_list
        self.num_per_team = per_team
        self.num_teams = num_teams

        self.solution = []
        self.last_fits = []
        self.solution_fit = 0

    def solve(self):
        population = self.init_pop(self.size)

        elite, top_fit = [], 696969696969 #random big number
        for g in range(self.generations):
            fit = [self.fitness(c) for c in population]
            elite, top_fit = self.select_elite(population, fit)
            
            self.solution = elite[0]
            self.solution_fit = top_fit
            self.last_fits.append(top_fit)
            print(f"generation {g+1} -> best fitness: {top_fit}")
            if top_fit == 0:
                break
#             if self.last_fits.count(top_fit)>self.generations/2:
#                 break

            population = self.breed(elite)
        
        return self.solution

    def init_pop(self, n):
        pop = []
        for _ in range(n):
            pop.append(self.random_chromosome())
        
        return pop

    def select_elite(self, population, fitness):
        indx = sorted(range(len(population)), key=lambda k: fitness[k])
        return [population[i] for i in indx[:self.top_select]], fitness[indx[0]]
    
    def select_top_mut(self, mutations, fitness):
        indx = sorted(range(len(mutations)), key=lambda k: fitness[k])
        return mutations[indx[0]], fitness[indx[0]]

    def random_chromosome(self):
        rand.shuffle(self.players)
        chunks = list(Utils.chunks(self.players, self.num_per_team))
        for i in range(len(chunks)):
            chunks[i] = ["" , chunks[i]]
        return chunks
    
    def breed_elite(self, population, elite_muts = 5):
        for i,c in enumerate(population):
            muts = []
            for _ in range(elite_muts):
                muts.append(self.mutate(copy.deepcopy(c)))
            mut_fits = [self.fitness(m) for m in muts]
            fittest_mut, mut_fit = self.select_top_mut(muts, mut_fits)
            if mut_fit>self.fitness(c):
                population[i] = fittest_mut
        
        return population

    def breed(self, elite):
        # elite = copy.deepcopy(elite)
        elite = self.breed_elite(elite) #elitism + allowing mutations within elite

        for c in range(self.size - len(elite)): #took out crossover since it was making the algorithm take too long; this problem isn't the best application for genetic algorithm anyways, but whatever
            #p1 = rand.choice(elite)
            #p2 = rand.choice(elite)
            #child = self.crossover(p1, p2)
            child = self.mutate(copy.deepcopy(rand.choice(elite)))
            
            elite.append(child)

        return elite

    def fitness(self, chromosome):
        fitness = 0
        seen_tags = []

        for group in chromosome:
            possible = self.findTag(group[1])
            if len(possible[0])>0:
                longest_tag = possible[0]
            else:
                longest_tag = max(possible, key=len)
            group[0] = longest_tag
            if longest_tag =="":
                fitness+=5000
            else:
                if longest_tag in seen_tags:
                    fitness+=500
                else:
                    seen_tags.append(longest_tag)  
                if possible.index(longest_tag)!=0:
                    if possible.index(longest_tag) == 1:
                        fitness+=250
                        
                    elif possible.index(longest_tag) == 2:
                        fitness += 175   
            
            # if len(group[1])!=self.num_per_team:
            #     fitness+=1000
            for player in group[1]:
                if not player.startswith(longest_tag):
                    fitness+=50
                # other_fit = self.fit_other_better(group, player, chromosome)
                # if other_fit[0]:
                #     fitness+=250*other_fit[1]
        return fitness
    
    def findTag(self,group):
        #check prefix
        pre = commonprefix(group)
        
        #check suffix
        suf = commonprefix(list(map(lambda l: l[::-1], group)))[::-1]
        
        #check mixed affixes
        mixed = ''
        is_pre_suf, to_det = commonaffix(group)
        if is_pre_suf:
            mixed = to_det
       
        return pre.strip(), suf.strip(), mixed.strip()
    
    def fit_other_better(self,cur_group, player, chromosome):
        cur_tag = cur_group[0]
        count = 0
        for group in chromosome:
            if group==cur_group: continue

            possible_fit = max(self.findTag([group[0], player]), key=len)
            if len(possible_fit)>len(cur_tag) and len(possible_fit)>= len(group[0]):
                count+=1
        
        return (True, count) if count>0 else (False, 0)

    def crossover(self, p1, p2): #slows algorithm down because it creates child chromosomes with duplicate strings, which makes the solution completely useless
        r = rand.random()
        use_cut = p1 if r<0.5 else p2
        cutoff = rand.randint(0, len(use_cut)-1)
        return p1[:cutoff] + p2[cutoff:]
    
    def mutate(self, chromosome): #swap two strings
        if rand.random()<self.mut_rate:
            swap_from = rand.randint(0, len(chromosome)-1)
            swap_to = rand.randint(0, len(chromosome)-1)
            
            ch1 = rand.choice(chromosome[swap_from][1])
            ch2 = rand.choice(chromosome[swap_to][1])
            
            chromosome[swap_from][1].remove(ch1)
            chromosome[swap_from][1].append(ch2)
            chromosome[swap_to][1].remove(ch2)
            chromosome[swap_to][1].append(ch1)
        
        return chromosome


if __name__ == "__main__":
    # players = ["MV bob", "pringle@MV", "LTA", "LTA HELLO", "MVMVMV", "LTAX", "MV help", "val LTA", "poo LTA", "5headMV"]
    # players = list({'x#1':0, 'xxx':0, 'Ryan@X':0, '¢ant':0, 'coolio': 0, 'cool kid': 0, "GG EZ": 0, 'gas mob':0, "gassed up":0, "bb":0, "bro123":0, "batman":0}.keys())
    players = ['λρ Tom', 'A*', 'v¢ sauzule', 'saharave', 'MKW 4Beans', 'cadavreMK', 'coci loko', 'C', 'So[LLLLLL]', 'Zjazca', 'Z- stavros', 'vc Dane']
    players = list({'x#1':0, 'xxx':0, 'Ryan@X':0, '¢ant':0, 'coolio': 0, 'cool kid cool': 0, "GG EZ": 0, 'gas mob':0, "gassed up":0, "kaya yanar":0, "yaya kanar":0, "yaka ranar":0}.keys())
    players5 = list({'x#*********************ATSDUAJSDGHASDUYkajsdhalkjdh1':0, 'awasasasdasdasddsdadsddasdsadd':0, 'Ryadadadadddanasdasd@X':0, '¢unasdklajsdkajsdhalkjsddsasdasdt':0, 'stop asd;liajds;aosdij;alskdj;alsdkasdasdman': 0, 'coolasdasd kasdlkajsd;laksjdasdsadid cool': 0, "GG EaslkdjahsldkjadshlkajsdhlaksjdahsdasdZ": 0, 'gas moasdalkdsja;lsdb':0, "gasseasdasddsasasdd up":0, "kaya kljaxdlasdkasjdhalksdjhkjyanar":0, "yaya kasdaasdljsdhaosduy98712sdanar":0, "ya123123313233asdASDASDkqeeqweqwea ranar":0}.keys())
    players6 = list({'helasasdndkzxdkzjxdnzddasdlo':0, 'stupasdalasdsdasda  asda ds adsdasid':0, 'asdl;lajsdhalksdjhlaskdjhaoisudyoaisduVA':0, 'banvannnnansdasdnansdnsdnasdndansdansdasndned':0, '09a8sd79as8d7a9s8d7a9sd87a9sd90':0, 'heaqoiu1p2oiu12981y49yoiusdasdll&*':0, 'whaasdasldajdsh;akjdhlaksjdhladsdsasdasddaat?':0, "a;lsdkja;sldkja;dlkaj;daaslkdja;lsdkjasd;l ad92y?":0, "λxasdasdasd12131311231asddade":0, 'Aaasd;lkasjd;alskdj;alskdjsdasdasAA':0, 'λp fraasdaskdkhalksdasdasdadud':0, 'AasdlkajdlaasdasdsdasdkdsjhlaksdBB':0}.keys())
    players9 = list({'helasasdndkzxdkzjxdnzddasdlo':0, 'stupasdalasdsdasda  asda ds adsdasid':0, 'asdl;lajsdhalksdjhlaskdjhaoisudyoaisduVA':0, 'banvannnnansdasdnansdnsdnasdndansdansdasndned':0, '09a8sd79as8d7a9s8d7a9sd87a9sd90':0, 'heaqoiu1p2oiu12981y49yoiusdasdll&*':0, 'whaasdasldajdsh;akjdhlaksjdhladsdsasdasddaat?':0, "a;lsdkja;sldkja;dlkaj;daaslkdja;lsdkjasd;l ad92y?":0, "λxasdasdasd12131311231asddade":0, 'Aaasd;lkasjd;alskdj;alskdjsdasdasAA':0, 'λp fraasdaskdkhalksdasdasdadud':0, 'AasdlkajdlaasdasdsdasdkdsjhlaksdBB':0}.keys())
    players7 = list({'he1273182376198237619283716932llo':0, 'heasdaklsdhalisduyaosidu123':0, 'borrowasalsdjhalsdkjalsdkjdasded time':0, 'bannasdasdaded':0, 'barasdasdrasda;klsdjakldsjhasd9o8yael':0, 
                'hellas1o2y92yoiuasdasdasdasdasddlkjasdlkajdsl&*':0, 'whaskdjhadsklbccmzbnx,mzat?':0, "wasdasdasdlkahsdjho?":0, "λasdasdkjalshdlakshdo9yous&*^&(*&^(*^&%9aksjdhaasdlkasd9qweyasdxe":0, 'AAasldkjadslkjadkajhdslkajdhlaksjdhalsdkjhasdA':0, 'λpasdasdas asd;alisdha;lksdhlakdsfraud':0, 'whasd;laskdhasdkjhaosiduyas9od8as9d8yapsd9ere?':0}.keys())
    players8 = list({'helasdas1231y392y31o2dlo':0, 'stupasdaasasdasdasdddasddssdasid':0, 'asdl;lajsdhalksdjhlaskdjhaoisudyoaisduVA':0, 'banvannnnansdasdnansdnsdnasdndansdansdasndned':0, '09a8sd79as8d7a9s8d7a9sd87a9sd90':0, 'heaqoiu1p2oiu12981y49yoiusdasdll&*':0, 'whaasdasldajdsh;akjdhlaksjdhladsdsasdasddaat?':0, "whasdasdasdasdasdo?":0, "λxasdasdasdasddade":0, 'Aaasd;lkasjd;alskdj;alskdjsdasdasAA':0, 'λp fraasdahdsdo9oysda2eoiu oi u  lajsd lassdasdadud':0, 'Aasdlkasdlkj lkj asdadasdajdlakdsjhlaksdBB':0}.keys())
                
    players4 = list({'pringleMVMMVMVMVMVMVMVMVMVMVMMVMV@MV':0,'5heaskdjhadslkajhdslakhdaiuyo876o876o8768asdadMV':0,'hellasjdhahksdjhalskdjhalsdkjhaldo LTA':0,'Lasdkjahdklajsdhaosd98odTAX':0,
            'jaja Lasdkjhdslaiusdyoasudyoasyasdya0sddTA':0,'stupasldasldkj;sdkaj;sdalkdsj;asldkid@LTA':0,'poop asdlakjdshlakjdshadssdMV':0,'MVMVMasdklahdsldssaadVMV':0,'LTA Vvalksjlpvalkjalksuqwealpo':0,"5 guys glajshdl asjh mom's spaghet":0}.keys())
    players = list({'x#*(*&(&(*&(*&(*&akjsdhasd87asd6a8sd11':0, 'xxxXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':0, 'Ryan@XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX':0, '¢uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuunt':0, 'coolllllllllllkjkjkjkj123l12jk1jlio': 0, 'cool k12o381 102u 2oi1u 2id cool': 0, "GG EZZZZZZZZZZZZZZZZZZZZZZZZZ": 0, 'gas masd12o31uy2398   asdasadsadadsaob':0, "gassessssssssssssssssssd up":0, "kayajksdhasuoday9y098709a yanar":0, "yaya kasmasklaslkadsljladskjldsanar":0, "yaka kakaakakakdskdskasdadsjdsakranar":0}.keys())
    players2 = ['asldkjadheaslkjdaskjdhlaksjdahdsllo', 'hasd123123213.kjadshaliskdjho876e123', 'borrowed timasd;laasdllndlksdhaposdu98q2ee', 'WAasd.kj.asdas.da.dsasd.asd.asd.a adshiaosda8dsX', 'basdkjasda  sda qe e j12oei1eahdlkajdsyao8ds7yarrel', 
                'A-asdlkadslkajdhlla192837192akjsdh1', 'whasdoqiouewiuy12o13y4183476184716894124at?', "WWW.Pasdalj;lsdhaldksjhlkaH.COM", "λxeasdlkahdsasdsd ds adaalsda98", 'Aasdlkaskldjahsd9a8y-2', 'λp frasdjlhalkdsjsasdlaksjdhadsd90ayaud', 'WOwowowowowowowowowowoowowowowowowW!!']
    players3 = ['λρ ToOOOOOOOOOOOOOOoooooooooooom', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA*', 'v¢ bvbvbvvvvvvvvvvvvvvvvvvvvvvvvvvvvvbvbvbvbvsauzule', 'sahasdjasdkjadshlkajsdhlakdsarave', 'MasdkjjdslakjdshlaksdjhKW 4Beans', 'cadasdasldhadjh9y01984y1944144avreMK', 'cocia;lskdhklajsdhasdo9y loko', 'Casdkjadhlajdasdasdhlkdsho9shap9sd8y', 'So[akjsdhakljdshaoisduyads8yLLLLLL]', 'Zjazasda,smdda   asddnadsasdasdca', 'Z- stavrosaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa']
    players+=players2+players7+players8+players4+players5+players6+players3+players9*25
    
    players = list(map(lambda l: Utils.sanitize_uni(l.strip()).lower(), players))
    tagalgo = GenAlgo(players, 6, 2)
    tick = time.time()
    final = tagalgo.solve()
    print('\nsolution:', final)
    
    print("algo time:", time.time()-tick)
    
    
