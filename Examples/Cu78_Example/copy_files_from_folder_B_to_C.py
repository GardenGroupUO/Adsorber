from Adsorber import Copy_Files_from_Folder_B_to_Folder_C

adsorbates = ['COH'] # 'CO', 'COOH', 'CHO', 

top_sites = {'Weird_Sites_Yellow': '89 96 98 102 115 121 131 135', '5_Fold_Vertex_Site_Red':'104 126', 'Weird_Corners_Blue':'92 93 132', 'Ico_Sites_Green':'106:109 112 113 118 119 124 130', 'Other_Weird_Sites_Orange': '84 86 88 94 95 97 99 105 111 114 116 122 123 125 127 129'}
bridge_sites = {'Weird_Sites_Yellow':'100 109 114 115 119:122 132 135 141:143 148 149 160 171', 'Other_5_fold_Sites_Blue':'99 123 126 127 130 131 150 152 157 158 227 229 241 245', 'Ico_Like_Green':'155 164 173:188 191 193 195 197:204 214 217:223 225 228 235 242 244'}
bridge_sites['Sites_Around_5_Fold_Vertex_Site_Orange'] = '106 111 112 134 136:138 140 144 146 151 194 205 206 209:211 213 230 232 233 239'
three_fold_sites = {'Weird_Sites_Yellow':'93 95 97 98 101 102 106 109:111 114:117 120 125 136 137 145 174:176 187', 'Ico_Like_Green':'132 133 138:140 147:163 165:170 178:186 191'}
three_fold_sites['Other_Sites_Around_5_Fold_Vertex_Site_Orange'] = '99 100 103 104 108 119 121 126 131 164 171'
four_fold_sites = {}

Copy_Files_from_Folder_B_to_Folder_C(adsorbates, top_sites, bridge_sites, three_fold_sites, four_fold_sites)
