# 元素筛选--成功--共9条筛选
import os
import json
import shutil
import xmltodict
import lxml.etree

folder_read = "/users/gracekoo/University/Project/Data/ProjectDocument/t1/"      
f_write = "/users/gracekoo/University/Project/Data/ProjectDocument/t2/Extract.txt" 

files_read = os.listdir(folder_read)

fw = open(f_write,"w+")
fw.write("自首\t无证驾驶\t死亡人数\t认罪态度\t是否谅解\t事故处理态度\t积极赔偿\t主刑\t法条\n")

for file in files_read:
    print(folder_read + file)
    fr = open(folder_read + file)
    
    text = xmltodict.parse(fr.read().encode('utf-8'))
    s = json.loads(json.dumps(text))
    print(len(s))
    flag = False
    try:
        #Surrender
        lxqj = s['writ']['QW']['CPFXGC']['LXQJ']
        if 'FDLXQJ' in lxqj:
            Surrender = lxqj['FDLXQJ']['QJ']['@value']
        else:
            Surrender = "否"
        
        
        
        #NoLicense
        if "无证驾驶" in s['writ']['QW']['CPFXGC']['@value']:
            NoLicense = "是"
        else:
            NoLicense = "否"
        
       
        
        #Dies
        dies = 0
        if 'BHR' in s['writ']['QW']['AJJBQK']:
            bhr_list = s['writ']['QW']['AJJBQK']['BHR']
            if type(bhr_list) is list:
                for bhr in bhr_list:
                    if bhr['SFSW']['@value'] == "是":
                        dies += 1
            elif type(bhr_list) is dict:
                if bhr_list['SFSW']['@value'] == "是":
                    dies += 1
        
        
        
        #SAttitude,Excuse,AAttitude
        SAttitude = "不知"
        Excuse = "不知"
        AAttitude = "不知"
        if 'ZDLXQJ' in s['writ']['QW']['CPFXGC']['LXQJ']:
            zdlxqj_type = s['writ']['QW']['CPFXGC']['LXQJ']['ZDLXQJ']
            if type(zdlxqj_type) is list:
                for zdlxqj in zdlxqj_type:
                    if zdlxqj['QJ']['@value'] == "认罪态度好":
                        SAttitude = "态度好"
                    elif "谅解" in zdlxqj['QJ']['@value']:
                        Excuse = "谅解"
                    elif "采取补救措施" in zdlxqj['QJ']['@value']:
                        AAttitude = "补救"
                        break
            
            elif type(zdlxqj_type) is dict:
                if zdlxqj_type['QJ']['@value'] == "认罪态度好":
                    SAttitude = "态度好"
                elif "谅解" in zdlxqj['QJ']['@value']:
                    Excuse = "谅解"
                elif "采取补救措施" in zdlxqj['QJ']['@value']:
                        AAttitude = "补救"
               
        #PCompensate
        if "积极赔偿" in s['writ']['QW']['@value']:
            PCompensate = "积极"
        else:
            PCompensate = "不积极"
                
        #Result_MainS
        Result_MainS = s['writ']['QW']['PJJG']['XSPJJGFZ']['BSPJJG']['ZXPF']['ZX']['ZXXQ']['@value']
                
        #Law
        Law_list = ""
        if 'CUS_FLFT_RY' in s['writ']['QW']['CPFXGC']['CUS_FLFT_FZ_RY']:
            law_type = s['writ']['QW']['CPFXGC']['CUS_FLFT_FZ_RY']['CUS_FLFT_RY']
            print("law_list",type(law_type))
            if type(law_type) is list:
                for law in law_type:
                    Law_list += law['@value'] + "\n"
                      
            elif type(law_type) is dict:
                Law_list += law['@value']
        
       
        
        fw.write(Surrender +"\t"+ NoLicense  +"\t"+ str(dies) +"\t"+ SAttitude +"\t" + 
                 Excuse +"\t"+ AAttitude +"\t"+ PCompensate +"\t"+ Result_MainS +"\t"+ Law_list + "\n")
        fr.close()
        
        print()
        
    except e:
        print(e)
        continue
        
fw.close()