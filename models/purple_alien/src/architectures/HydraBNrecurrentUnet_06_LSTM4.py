
import torch
import torch.nn as nn
import torch.nn.functional as F

# why can't import????
# give everything better names at some point
class HydraBNUNet06_LSTM4(nn.Module):
    def __init__(self, input_channels, total_hidden_channels, output_channels, dropout_rate):
        super().__init__()

        kernel_size = 3 
        base = total_hidden_channels # The fact that these are the same is legacy from when this was an RNN. It works, but it could be changed to something else.
        lstm_padding = kernel_size // 2 # only use in the LSTM
        
        num_lstm_cells = 4 # could and should be hyperparameter to takes the vaules 1,2,3,4, 8, 16.
        num_lstm_state_layers = int(total_hidden_channels/(num_lstm_cells*2)) # *2 because both hs (short-term) and hl (long-term). This diffinetion ensures the number of total layers does not change when you change the number of lstm cells. But it could be changed to something else.
        
        self.base = base # to extract later
        
        # encoder (downsampling)
        self.enc_conv0 = nn.Conv2d(input_channels + int(total_hidden_channels/2), base, kernel_size, padding=1, bias = False) #input channels + total_hidden_channels) because you only concat x with hs and not hl. So it will always be half.

        self.bn_enc_conv0 = nn.BatchNorm2d(base)
        self.pool0 = nn.MaxPool2d(2, 2, padding=0) # 16 -> 8

        self.enc_conv1 = nn.Conv2d(base, base*2, kernel_size, padding=1, bias = False)
        self.bn_enc_conv1 = nn.BatchNorm2d(base*2) 
        self.pool1 = nn.MaxPool2d(2, 2, padding=0) # 8 -> 4

        # bottleneck
        self.bottleneck_conv = nn.Conv2d(base*2, base*4, kernel_size, padding=1, bias = False)
        self.bn_bottleneck_conv = nn.BatchNorm2d(base*4) 
        

        # HEAD1 reg
        self.upsample0_head1_reg = nn.ConvTranspose2d(base*4, base*2, 2, stride= 2, padding= 0, output_padding= 0) # 4 -> 8
        self.dec_conv0_head1_reg = nn.Conv2d(base*4, base*2, kernel_size, padding=1, bias = False) # base+base=base*2 because of skip conneciton
        self.bn_dec_conv0_head1_reg = nn.BatchNorm2d(base*2) 

        self.upsample1_head1_reg = nn.ConvTranspose2d(base*2, base, 2, stride= 2, padding= 0, output_padding= 0) # 8 -> 16
        self.dec_conv1_head1_reg = nn.Conv2d(base*2, base, kernel_size, padding=1, bias = False) # base+base=base*2 because of skip connection
        self.bn_dec_conv1_head1_reg = nn.BatchNorm2d(base) 

        self.dec_conv4_head1_reg = nn.Conv2d(base, output_channels, kernel_size, padding=1) # 2 because reg and class


        # HEAD1 class
        self.upsample0_head1_class = nn.ConvTranspose2d(base*4, base*2, 2, stride= 2, padding= 0, output_padding= 0) # 4 -> 8
        self.dec_conv0_head1_class = nn.Conv2d(base*4, base*2, kernel_size, padding=1, bias = False) # base+base=base*2 because of skip conneciton
        self.bn_dec_conv0_head1_class = nn.BatchNorm2d(base*2) 

        self.upsample1_head1_class = nn.ConvTranspose2d(base*2, base, 2, stride= 2, padding= 0, output_padding= 0) # 8 -> 16
        self.dec_conv1_head1_class = nn.Conv2d(base*2, base, kernel_size, padding=1, bias = False) # base+base=base*2 because of skip connection
        self.bn_dec_conv1_head1_class = nn.BatchNorm2d(base) 

        self.dec_conv4_head1_class = nn.Conv2d(base, output_channels, 3, padding=1)
        

        # HEAD2 reg
        self.upsample0_head2_reg = nn.ConvTranspose2d(base*4, base*2, 2, stride= 2, padding= 0, output_padding= 0) # 4 -> 8
        self.dec_conv0_head2_reg = nn.Conv2d(base*4, base*2, kernel_size, padding=1, bias = False) # base+base=base*2 because of skip conneciton
        self.bn_dec_conv0_head2_reg = nn.BatchNorm2d(base*2) 

        self.upsample1_head2_reg = nn.ConvTranspose2d(base*2, base, 2, stride= 2, padding= 0, output_padding= 0) # 8 -> 16
        self.dec_conv1_head2_reg = nn.Conv2d(base*2, base, kernel_size, padding=1, bias = False) # base+base=base*2 because of skip connection
        self.bn_dec_conv1_head2_reg = nn.BatchNorm2d(base) 

        self.dec_conv4_head2_reg = nn.Conv2d(base, output_channels, 3, padding=1) # 2 because reg and class


        # HEAD2 class
        self.upsample0_head2_class = nn.ConvTranspose2d(base*4, base*2, 2, stride= 2, padding= 0, output_padding= 0) # 4 -> 8
        self.dec_conv0_head2_class = nn.Conv2d(base*4, base*2, kernel_size, padding=1, bias = False) # base+base=base*2 because of skip conneciton
        self.bn_dec_conv0_head2_class = nn.BatchNorm2d(base*2) 

        self.upsample1_head2_class = nn.ConvTranspose2d(base*2, base, 2, stride= 2, padding= 0, output_padding= 0) # 8 -> 16
        self.dec_conv1_head2_class = nn.Conv2d(base*2, base, kernel_size, padding=1, bias = False) # base+base=base*2 because of skip connection
        self.bn_dec_conv1_head2_class = nn.BatchNorm2d(base) 

        self.dec_conv4_head2_class = nn.Conv2d(base, output_channels, kernel_size, padding=1)


        # HEAD3 reg
        self.upsample0_head3_reg = nn.ConvTranspose2d(base*4, base*2, 2, stride= 2, padding= 0, output_padding= 0) # 4 -> 8
        self.dec_conv0_head3_reg = nn.Conv2d(base*4, base*2, kernel_size, padding=1, bias = False) # base+base=base*2 because of skip conneciton
        self.bn_dec_conv0_head3_reg = nn.BatchNorm2d(base*2) 

        self.upsample1_head3_reg = nn.ConvTranspose2d(base*2, base, 2, stride= 2, padding= 0, output_padding= 0) # 8 -> 16
        self.dec_conv1_head3_reg = nn.Conv2d(base*2, base, kernel_size, padding=1, bias = False) # base+base=base*2 because of skip connection
        self.bn_dec_conv1_head3_reg = nn.BatchNorm2d(base) 

        self.dec_conv4_head3_reg = nn.Conv2d(base, output_channels, kernel_size, padding=1) # 2 because reg and class


        # HEAD3 class
        self.upsample0_head3_class = nn.ConvTranspose2d(base*4, base*2, 2, stride= 2, padding= 0, output_padding= 0) # 4 -> 8
        self.dec_conv0_head3_class = nn.Conv2d(base*4, base*2, 3, padding=1, bias = False) # base+base=base*2 because of skip conneciton
        self.bn_dec_conv0_head3_class = nn.BatchNorm2d(base*2) 

        self.upsample1_head3_class = nn.ConvTranspose2d(base*2, base, 2, stride= 2, padding= 0, output_padding= 0) # 8 -> 16
        self.dec_conv1_head3_class = nn.Conv2d(base*2, base, kernel_size, padding=1, bias = False) # base+base=base*2 because of skip connection
        self.bn_dec_conv1_head3_class = nn.BatchNorm2d(base) 

        self.dec_conv4_head3_class = nn.Conv2d(base, output_channels, kernel_size, padding=1)

        # Dropout
        self.dropout = nn.Dropout(p = dropout_rate)

        # LSTM

        # LSTM 1
        self.Wxi_1 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True) 
        self.Whi_1 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Wxf_1 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Whf_1 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Wxc_1 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Whc_1 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Wxo_1 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Who_1 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)


        # LSTM 2
        self.Wxi_2 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Whi_2 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Wxf_2 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Whf_2 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Wxc_2 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Whc_2 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Wxo_2 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Who_2 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)


        # LSTM 3
        self.Wxi_3 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True) 
        self.Whi_3 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Wxf_3 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Whf_3 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Wxc_3 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Whc_3 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Wxo_3 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Who_3 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)


        # LSTM 4
        self.Wxi_4 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True) 
        self.Whi_4 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Wxf_4 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Whf_4 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Wxc_4 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Whc_4 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Wxo_4 = nn.Conv2d(input_channels, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)
        self.Who_4 = nn.Conv2d(num_lstm_state_layers, num_lstm_state_layers, kernel_size, padding=lstm_padding, bias=True)


    def forward(self, x, h):

        # Splitting the hidden state tensor into 4 short-term memory tensors and 4 long-term memory tensors. 
        split_h = int(h.shape[1] / 8) # 32/8 = 4. 32 is the dim of the full hidden state. 8 is the number of tensors we want to split it into. Each tensor is then 4 channels.
        hs_1, hs_2, hs_3, hs_4, hl_1, hl_2, hl_3, hl_4 = torch.split(h, split_h, dim=1) 

        #----------------- LSTM 1 -----------------
        # Input gate
        i_t_1 = torch.sigmoid(self.Wxi_1(x) + self.Whi_1(hs_1)) # Wxi changes to dims for x to the same as hs
        # Forget gate
        f_t_1 = torch.sigmoid(self.Wxf_1(x) + self.Whf_1(hs_1)) # Wxf changes to dims for x to the same as hs
        # Cell state
        hl_1_tilde = torch.tanh(self.Wxc_1(x) + self.Whc_1(hs_1)) # Wxc changes to dims for x to the same as hs
        hl_1 = f_t_1 * hl_1 + i_t_1 * hl_1_tilde
        # Output gate
        o_t_1 = torch.sigmoid(self.Wxo_1(x) + self.Who_1(hs_1)) # Wxo changes to dims for x to the same as hs
        
        hs_1 = o_t_1 * torch.tanh(hl_1) # The "input" that is used in the U-net below

        #----------------- LSTM 2 -----------------
        # Input gate
        i_t_2 = torch.sigmoid(self.Wxi_2(x) + self.Whi_2(hs_2)) # Wxi changes to dims for x to the same as hs
        # Forget gate
        f_t_2 = torch.sigmoid(self.Wxf_2(x) + self.Whf_2(hs_2)) # Wxf changes to dims for x to the same as hs
        # Cell state
        hl_2_tilde = torch.tanh(self.Wxc_2(x) + self.Whc_2(hs_2)) # Wxc changes to dims for x to the same as hs
        hl_2 = f_t_2 * hl_2 + i_t_2 * hl_2_tilde
        # Output gate
        o_t_2 = torch.sigmoid(self.Wxo_2(x) + self.Who_2(hs_2)) # Wxo changes to dims for x to the same as hs
        
        hs_2 = o_t_2 * torch.tanh(hl_2) # The "input" that is used in the U-net below

        #----------------- LSTM 3 -----------------
        # Input gate
        i_t_3 = torch.sigmoid(self.Wxi_3(x) + self.Whi_3(hs_3)) # Wxi changes to dims for x to the same as hs
        # Forget gate
        f_t_3 = torch.sigmoid(self.Wxf_3(x) + self.Whf_3(hs_3)) # Wxf changes to dims for x to the same as hs
        # Cell state
        hl_3_tilde = torch.tanh(self.Wxc_3(x) + self.Whc_3(hs_3)) # Wxc changes to dims for x to the same as hs
        hl_3 = f_t_3 * hl_3 + i_t_3 * hl_3_tilde
        # Output gate
        o_t_3 = torch.sigmoid(self.Wxo_3(x) + self.Who_3(hs_3)) # Wxo changes to dims for x to the same as hs

        hs_3 = o_t_3 * torch.tanh(hl_3) # The "input" that is used in the U-net below

        #----------------- LSTM 4 -----------------
        # Input gate
        i_t_4 = torch.sigmoid(self.Wxi_4(x) + self.Whi_4(hs_4)) # Wxi changes to dims for x to the same as hs
        # Forget gate
        f_t_4 = torch.sigmoid(self.Wxf_4(x) + self.Whf_4(hs_4)) # Wxf changes to dims for x to the same as hs
        # Cell state
        hl_4_tilde = torch.tanh(self.Wxc_4(x) + self.Whc_4(hs_4)) # Wxc changes to dims for x to the same as hs
        hl_4 = f_t_4 * hl_4 + i_t_4 * hl_4_tilde
        # Output gate
        o_t_4 = torch.sigmoid(self.Wxo_4(x) + self.Who_4(hs_4)) # Wxo changes to dims for x to the same as hs

        hs_4 = o_t_4 * torch.tanh(hl_4) # The "input" that is used in the U-net below
        
        # -----------------
        h = torch.cat([hs_1, hs_2, hs_3, hs_4, hl_1, hl_2, hl_3, hl_4], 1) # concatenating short and long term memory along the channels. What is carried forward to the next timestep. The concat is just to keep it tight...
        # -----------------

        x = torch.cat([x, hs_1, hs_2, hs_3, hs_4], 1) # concatenating x and the new short term memory along the channels - x here as a skip connection

        # encoder
        e0s_ = F.relu(self.bn_enc_conv0(self.enc_conv0(x))) 

        e0s = self.dropout(e0s_)
        e0 = self.pool0(e0s)
        
        e1s = self.dropout(F.relu(self.bn_enc_conv1(self.enc_conv1(e0))))
        e1 = self.pool1(e1s)

        # bottleneck
        b = F.relu(self.bn_bottleneck_conv(self.bottleneck_conv(e1)))
        b = self.dropout(b)

        # DECODERS #
        #H1 reg
        H1_d0 = F.relu(self.bn_dec_conv0_head1_reg(self.dec_conv0_head1_reg(torch.cat([self.upsample0_head1_reg(b),e1s],1))))
        H1_d0 = self.dropout(H1_d0)
        
        H1_d1 = F.relu(self.bn_dec_conv1_head1_reg(self.dec_conv1_head1_reg(torch.cat([self.upsample1_head1_reg(H1_d0), e0s],1)))) # You did not have any activations before - why not?
        H1_reg = self.dropout(H1_d1)

        H1_reg = self.dec_conv4_head1_reg(H1_reg)
        
        out_reg1 = F.relu(H1_reg)

        #H1 class
        H1_d0 = F.relu(self.bn_dec_conv0_head1_class(self.dec_conv0_head1_class(torch.cat([self.upsample0_head1_class(b),e1s],1))))
        H1_d0 = self.dropout(H1_d0)
        
        H1_d1 = F.relu(self.bn_dec_conv1_head1_class(self.dec_conv1_head1_class(torch.cat([self.upsample1_head1_class(H1_d0), e0s],1)))) # You did not have any activations before - why not?
        H1_class = self.dropout(H1_d1)

        # H1_d2 = F.relu(self.bn_dec_conv2_head1_class(self.dec_conv2_head1_class(H1_d1)))
        # H1_d2 = self.dropout(H1_d2) # is this good?
        
        # H1_class = F.relu(self.bn_dec_conv3_head1_class(self.dec_conv3_head1_class(H1_d2)))
        # H1_class = self.dropout(H1_class) # is this good?
        
        H1_class = self.dec_conv4_head1_class(H1_class)

        out_class1 = H1_class # torch.sigmoid(H1_class) # could move sigmoid outta here...


        #H2 reg
        H2_d0 = F.relu(self.bn_dec_conv0_head2_reg(self.dec_conv0_head2_reg(torch.cat([self.upsample0_head2_reg(b),e1s],1))))
        H2_d0 = self.dropout(H1_d0)
        
        H2_d1 = F.relu(self.bn_dec_conv1_head2_reg(self.dec_conv1_head2_reg(torch.cat([self.upsample1_head2_reg(H2_d0), e0s],1)))) # You did not have any activations before - why not?
        H2_reg = self.dropout(H1_d1)

        # H2_d2 = F.relu(self.bn_dec_conv2_head2_reg(self.dec_conv2_head2_reg(H2_d1)))
        # H2_d2 = self.dropout(H1_d2) # is this good?

        # H2_reg = F.relu(self.bn_dec_conv3_head2_reg(self.dec_conv3_head2_reg(H2_d2)))
        # H2_reg = self.dropout(H2_reg) # is this good?
        
        H2_reg = self.dec_conv4_head2_reg(H2_reg)
        
        out_reg2 = F.relu(H2_reg)

        #H2 class
        H2_d0 = F.relu(self.bn_dec_conv0_head2_class(self.dec_conv0_head2_class(torch.cat([self.upsample0_head2_class(b),e1s],1))))
        H2_d0 = self.dropout(H1_d0)
        
        H2_d1 = F.relu(self.bn_dec_conv1_head2_class(self.dec_conv1_head2_class(torch.cat([self.upsample1_head2_class(H2_d0), e0s],1)))) # You did not have any activations before - why not?
        H2_class = self.dropout(H2_d1)

        # H2_d2 = F.relu(self.bn_dec_conv2_head2_class(self.dec_conv2_head2_class(H2_d1)))
        # H2_d2 = self.dropout(H1_d2) # is this good?
        
        # H2_class = F.relu(self.bn_dec_conv3_head2_class(self.dec_conv3_head2_class(H2_d2)))
        # H2_class = self.dropout(H2_class) # is this good?
        
        
        H2_class = self.dec_conv4_head2_class(H2_class)

        out_class2 = H2_class # torch.sigmoid(H1_class) # could move sigmoid outta here...



        #H3 reg
        H3_d0 = F.relu(self.bn_dec_conv0_head3_reg(self.dec_conv0_head3_reg(torch.cat([self.upsample0_head3_reg(b),e1s],1))))
        H3_d0 = self.dropout(H3_d0)
        
        H3_d1 = F.relu(self.bn_dec_conv1_head3_reg(self.dec_conv1_head3_reg(torch.cat([self.upsample1_head3_reg(H3_d0), e0s],1)))) # You did not have any activations before - why not?
        H3_reg = self.dropout(H3_d1)

        # H3_d2 = F.relu(self.bn_dec_conv2_head3_reg(self.dec_conv2_head3_reg(H3_d1)))
        # H3_d2 = self.dropout(H1_d2) # is this good?

        # H3_reg = F.relu(self.bn_dec_conv3_head3_reg(self.dec_conv3_head3_reg(H3_d2)))
        # H3_reg = self.dropout(H3_reg) # is this good?
        
        
        H3_reg = self.dec_conv4_head3_reg(H3_reg)
        
        out_reg3 = F.relu(H3_reg)

        #H3 class
        H3_d0 = F.relu(self.bn_dec_conv0_head3_class(self.dec_conv0_head3_class(torch.cat([self.upsample0_head3_class(b),e1s],1))))
        H3_d0 = self.dropout(H1_d0)
        
        H3_d1 = F.relu(self.bn_dec_conv1_head3_class(self.dec_conv1_head3_class(torch.cat([self.upsample1_head3_class(H3_d0), e0s],1)))) # You did not have any activations before - why not?
        H3_class = self.dropout(H3_d1)

        # H3_d2 = F.relu(self.bn_dec_conv2_head3_class(self.dec_conv2_head3_class(H3_d1)))
        # H3_d2 = self.dropout(H1_d2) # is this good?
        
        # H3_class = F.relu(self.bn_dec_conv3_head3_class(self.dec_conv3_head3_class(H3_d2)))
        # H3_class = self.dropout(H3_class) # is this good?
        
        
        H3_class = self.dec_conv4_head3_class(H3_class)

        out_class3 = H3_class # torch.sigmoid(H1_class) # could move sigmoid outta here...


        # RESTRUCTURE TO FIT "OLD" FORMAT. dim 1 should be depth
        out_reg = torch.concat([out_reg1, out_reg2, out_reg3], dim=1)        
        out_class = torch.concat([out_class1, out_class2, out_class3], dim=1)

        return out_reg, out_class, h # e0s here also hidden state - should take tanh of self.enc_conv0(x) but it does not appear to make a big difference....


    def init_h(self, hidden_channels, dim): # could have x as input and then take x.shape

        hs = torch.zeros((1,hidden_channels,dim,dim), dtype= torch.float64)
        
        return hs 

    def init_hTtime(self, hidden_channels, H, W):
        
        # works
        hs = torch.abs(torch.randn((1,hidden_channels, H, W), dtype= torch.float64) * torch.exp(torch.tensor(-100))) 
        hs = torch.zeros((1,hidden_channels, H, W), dtype= torch.float64)

        return hs
