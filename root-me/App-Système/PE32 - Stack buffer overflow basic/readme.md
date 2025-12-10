
<img width="603" height="42" alt="image" src="https://github.com/user-attachments/assets/b7469530-04f3-4b2a-ada0-c791822d5f24" />


<img width="618" height="84" alt="image" src="https://github.com/user-attachments/assets/0775b3a2-891d-4073-b22a-71f28ad74684" />



<img width="789" height="21" alt="image" src="https://github.com/user-attachments/assets/2d7e3bdc-02cd-413e-a909-eae8f02b976e" />


<img width="1301" height="123" alt="image" src="https://github.com/user-attachments/assets/8ce4c94f-f8c9-4ec9-8220-2e65be858fb2" />




On sait que :

buff = 16 octets

sur un prologue standard 32-bit GCC/MinGW :

4 octets = EBP sauvegardé

4 octets = EIP retour

Donc 16 + 4 + 4 = 24.

→ C’est pourquoi la plupart des challenges avec ce code donnent 24.




<img width="474" height="71" alt="image" src="https://github.com/user-attachments/assets/ff9c6dfd-a706-4fc9-830e-4e552e50dbf4" />
