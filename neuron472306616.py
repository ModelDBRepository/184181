'''
Defines a class, Neuron472306616, of neurons from Allen Brain Institute's model 472306616

A demo is available by running:

    python -i mosinit.py
'''
class Neuron472306616:
    def __init__(self, name="Neuron472306616", x=0, y=0, z=0):
        '''Instantiate Neuron472306616.
        
        Parameters:
            x, y, z -- position offset
            
        Note: if name is not specified, Neuron472306616_instance is used instead
        '''
                
        self._name = name
        # load the morphology
        from load_swc import load_swc
        load_swc('Pvalb-IRES-Cre_Ai14_IVSCC_-176848.03.01.01_470528201_m.swc', self,
                 use_axon=False, xshift=x, yshift=y, zshift=z)

        # custom axon (works because dropping axon during import)
        from neuron import h
        self.axon = [h.Section(cell=self, name='axon[0]'),
                     h.Section(cell=self, name='axon[1]')]
        for sec in self.axon:
            sec.L = 30
            sec.diam = 1
            sec.nseg = 1
        self.axon[0].connect(self.soma[0](0.5))
        self.axon[1].connect(self.axon[0](1))
        self.all += self.axon

        self._insert_mechanisms()
        self._discretize_model()
        self._set_mechanism_parameters()
    
    def __str__(self):
        if self._name is not None:
            return self._name
        else:
            return "Neuron472306616_instance"
                
    def _insert_mechanisms(self):
        from neuron import h
        for sec in self.all:
            sec.insert("pas")
        for mech in [u'CaDynamics', u'Ca_HVA', u'Ca_LVA', u'Ih', u'Im_v2', u'K_T', u'Kd', u'Kv2like', u'Kv3_1', u'NaV', u'SK']:
            self.soma[0].insert(mech)
    
    def _set_mechanism_parameters(self):
        from neuron import h
        for sec in self.all:
            sec.Ra = 55.01
            sec.e_pas = -85.5152397156
        
        for sec in self.axon:
            sec.cm = 1.77
            sec.g_pas = 0.000461723114894
        for sec in self.dend:
            sec.cm = 1.77
            sec.g_pas = 1.95861529313e-05
        for sec in self.soma:
            sec.cm = 1.77
            sec.ena = 53.0
            sec.ek = -107.0
            sec.gbar_Ih = 0.000231386
            sec.gbar_NaV = 0.0426554
            sec.gbar_Kd = 7.87967e-05
            sec.gbar_Kv2like = 0.0618697
            sec.gbar_Kv3_1 = 1.36589
            sec.gbar_K_T = 0.00387371
            sec.gbar_Im_v2 = 1.24518e-06
            sec.gbar_SK = 0.000427014
            sec.gbar_Ca_HVA = 0.00070334
            sec.gbar_Ca_LVA = 0.00607984
            sec.gamma_CaDynamics = 0.0158668
            sec.decay_CaDynamics = 48.6466
            sec.g_pas = 0.000495673
    
    def _discretize_model(self):
        for sec in self.all:
            sec.nseg = 1 + 2 * int(sec.L / 40)

