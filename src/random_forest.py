#0:平地驾驶
#1：上坡
#2：下坡
#3：侧滑
class RandomForest:
    @classmethod
    def add_vectors(cls, v1, v2):
        return [sum(i) for i in zip(v1, v2)]

    @classmethod
    def score(cls, input):
        var0 = var1 = var2 = var3 = var4 = var5 = var6 = var7 = var8 = [0.0, 0.0, 0.0, 0.0]

        if input[0] >= 2.238578552246094 and input[2] >= -9.219294299316406 and abs(input[1]) < 2.238578552246094:
            var0 = [0.0, 1.0, 0.0, 0.0]
        elif (input[0] < -2.238578552246094 and input[2] >= -9.219294299316406) and abs(input[1]) < 2.238578552246094:
            var0 = [0.0, 0.0, 1.0, 0.0]
        elif (abs(input[0]) < 2.238578552246094 and abs(input[1]) < 2.238578552246094) and input[2] < -9.219294299316406:
            var0 = [1.0, 0.0, 0.0, 0.0]
        elif abs(input[4]) >= 4.065721292316734:
            var0 = [0.0, 0.0, 0.0, 1.0]
            
        if input[30] >= 2.238578552246094 and input[32] >= -9.219294299316406 and abs(input[31]) < 2.238578552246094:
            var1 = [0.0, 1.0, 0.0, 0.0]
        elif (input[30] < -2.238578552246094 and input[32] >= -9.219294299316406) and abs(input[31]) < 2.238578552246094:
            var1 = [0.0, 0.0, 1.0, 0.0]
        elif (abs(input[30]) < 2.238578552246094 and abs(input[31]) < 2.238578552246094) and input[32] < -9.219294299316406:
            var1 = [1.0, 0.0, 0.0, 0.0]
        elif abs(input[34]) >= 4.065721292316734:
            var1 = [0.0, 0.0, 0.0, 1.0] 
            
        if input[60] >= 2.238578552246094 and input[62] >= -9.219294299316406 and abs(input[61]) < 2.238578552246094:
            var2 = [0.0, 1.0, 0.0, 0.0]
        elif (input[60] < -2.238578552246094 and input[62] >= -9.219294299316406) and abs(input[61]) < 2.238578552246094:
            var2 = [0.0, 0.0, 1.0, 0.0]
        elif (abs(input[60]) < 2.238578552246094 and abs(input[61]) < 2.238578552246094) and input[62] < -9.219294299316406:
            var2 = [1.0, 0.0, 0.0, 0.0]
        elif abs(input[64]) >= 4.065721292316734:
            var2 = [0.0, 0.0, 0.0, 1.0] 
            
        if input[90] >= 2.238578552246094 and input[92] >= -9.219294299316406 and abs(input[91]) < 2.238578552246094:
            var3 = [0.0, 1.0, 0.0, 0.0]
        elif (input[90] < -2.238578552246094 and input[92] >= -9.219294299316406) and abs(input[91]) < 2.238578552246094:
            var3 = [0.0, 0.0, 1.0, 0.0]
        elif (abs(input[90]) < 2.238578552246094 and abs(input[91]) < 2.238578552246094) and input[92] < -9.219294299316406:
            var3 = [1.0, 0.0, 0.0, 0.0]
        elif abs(input[94]) >= 4.065721292316734:
            var3 = [0.0, 0.0, 0.0, 1.0] 
            
        if input[90] >= 2.238578552246094 and input[92] >= -9.219294299316406 and abs(input[91]) < 2.238578552246094:
            var4 = [0.0, 1.0, 0.0, 0.0]
        elif (input[90] < -2.238578552246094 and input[92] >= -9.219294299316406) and abs(input[91]) < 2.238578552246094:
            var4 = [0.0, 0.0, 1.0, 0.0]
        elif (abs(input[90]) < 2.238578552246094 and abs(input[91]) < 2.238578552246094) and input[92] < -9.219294299316406:
            var4 = [1.0, 0.0, 0.0, 0.0]
        elif abs(input[94]) >= 4.065721292316734:
            var4 = [0.0, 0.0, 0.0, 1.0] 
            
        if input[120] >= 2.238578552246094 and input[122] >= -9.219294299316406 and abs(input[121]) < 2.238578552246094:
            var5 = [0.0, 1.0, 0.0, 0.0]
        elif (input[120] < -2.238578552246094 and input[122] >= -9.219294299316406) and abs(input[121]) < 2.238578552246094:
            var5 = [0.0, 0.0, 1.0, 0.0]
        elif (abs(input[120]) < 2.238578552246094 and abs(input[121]) < 2.238578552246094) and input[122] < -9.219294299316406:
            var5 = [1.0, 0.0, 0.0, 0.0]
        elif abs(input[124]) >= 4.065721292316734:
            var5 = [0.0, 0.0, 0.0, 1.0] 
        
        if input[150] >= 2.238578552246094 and input[152] >= -9.219294299316406 and abs(input[151]) < 2.238578552246094:
            var6 = [0.0, 1.0, 0.0, 0.0]
        elif (input[150] < -2.238578552246094 and input[152] >= -9.219294299316406) and abs(input[151]) < 2.238578552246094:
            var6 = [0.0, 0.0, 1.0, 0.0]
        elif (abs(input[150]) < 2.238578552246094 and abs(input[151]) < 2.238578552246094) and input[152] < -9.219294299316406:
            var6 = [1.0, 0.0, 0.0, 0.0]
        elif abs(input[154]) >= 4.065721292316734:
            var6 = [0.0, 0.0, 0.0, 1.0] 
        
        if input[180] >= 2.238578552246094 and input[182] >= -9.219294299316406 and abs(input[181]) < 2.238578552246094:
            var7 = [0.0, 1.0, 0.0, 0.0]
        elif (input[180] < -2.238578552246094 and input[182] >= -9.219294299316406) and abs(input[181]) < 2.238578552246094:
            var7 = [0.0, 0.0, 1.0, 0.0]
        elif (abs(input[180]) < 2.238578552246094 and abs(input[181]) < 2.238578552246094) and input[182] < -9.219294299316406:
            var7 = [1.0, 0.0, 0.0, 0.0]
        elif abs(input[184]) >= 4.065721292316734:
            var7 = [0.0, 0.0, 0.0, 1.0] 
            
        if input[210] >= 2.238578552246094 and input[212] >= -9.219294299316406 and abs(input[211]) < 2.238578552246094:
            var8 = [0.0, 1.0, 0.0, 0.0]
        elif (input[210] < -2.238578552246094 and input[212] >= -9.219294299316406) and abs(input[211]) < 2.238578552246094:
            var8 = [0.0, 0.0, 1.0, 0.0]
        elif (abs(input[210]) < 2.238578552246094 and abs(input[211]) < 2.238578552246094) and input[212] < -9.219294299316406:
            var8 = [1.0, 0.0, 0.0, 0.0]
        elif abs(input[214]) >= 4.065721292316734:
            var8 = [0.0, 0.0, 0.0, 1.0] 
            
        return cls.add_vectors(cls.add_vectors(cls.add_vectors(cls.add_vectors(cls.add_vectors(cls.add_vectors(cls.add_vectors(cls.add_vectors(var0, var1), var2), var3), var4), var5), var6), var7), var8)

    @classmethod
    def run(cls, input: list):
        res = cls.score(input)
        # print(res)
        return res.index(max(res))
# ...existing code...
